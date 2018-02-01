import json

import requests

from botal.datatypes import Message, UserInfo
from botal.messengesrs.messenger import Messenger


class Telegram(Messenger):
    def __init__(self, token, timeout=10):
        self._api_url = 'https://api.telegram.org/bot{}'.format(token)
        self._timeout = timeout
        self.cached_uploads = {}

    def _call_method(self, method, **kwargs):
        method_url = self._api_url + '/{}'.format(method)
        result = requests.post(method_url, params=kwargs)
        parsed = json.loads(result.text)
        return parsed

    def _send_attachment(self, chat_id, attachment):
        if attachment.url in self.cached_uploads and attachment.cache:
            return self.cached_uploads[attachment.url]

        upload_methods = {
            'image': ('photo', lambda x: self._call_method('sendPhoto', chat_id=chat_id, photo=x)),
            'video': ('video', lambda x: self._call_method('sendVideo', chat_id=chat_id, video=x)),
            'audio': ('audio', lambda x: self._call_method('sendAudio', chat_id=chat_id, audio=x)),
            'application': ('document', lambda x: self._call_method('sendDocument', chat_id=chat_id, document=x))
        }

        if attachment.url.startswith('file://'):
            file = open(attachment.url[:len('file://')], 'rb')
        elif attachment in self.cached_uploads:
            file = self.cached_uploads[attachment]
        else:
            file = attachment.url

        telegram_type, upload_method = upload_methods[attachment.file_type]
        file_id = upload_method(file)['result'][telegram_type]['file_id']

        if attachment.cache:
            self.cached_uploads[attachment] = file_id

    def listen(self):
        offset = None
        while True:
            kwargs = {'timeout': self._timeout}
            if offset is not None:
                kwargs.update({'offset': offset})
            result = self._call_method('getUpdates', **kwargs)

            for update in result['result']:
                offset = max(offset if offset else 0, update['update_id']) + 1

                yield Message(update['message']['text'], None), UserInfo(update['message']['chat']['id'], self)

    def send_message(self, user_id, text, attachments):
        self._call_method('sendMessage', chat_id=user_id, text=text)
        for attachment in attachments:
            self._send_attachment(user_id, attachment)


import json

import requests

from botal.datatypes import Message, User
from botal.messengesrs.messenger import Messenger


class Telegram(Messenger):
    def __init__(self, token, timeout=10):
        self._api_url = 'https://api.telegram.org/bot{}'.format(token)
        self._timeout = timeout
        self.cached_uploads = {}

    def _call_method(self, method, params, files):
        method_url = self._api_url + '/{}'.format(method)
        result = requests.post(method_url, params=params, files=files)
        parsed = json.loads(result.text)
        return parsed

    def _send_attachment(self, chat_id, attachment):
        if attachment.url in self.cached_uploads and attachment.cache:
            return self.cached_uploads[attachment.url]

        telegram_type = {
            'image': 'Photo',
            'video': 'Video',
            'audio': 'Audio',
            'application': 'Document'
        }[attachment.file_type]

        cached = attachment.get_cached(self)
        if cached is not None:
            message = self._call_method('send' + telegram_type,
                                        params={'chat_id': chat_id, telegram_type.lower(): cached}, files={})
        elif attachment.url.startswith('file://'):
            file = open(attachment.url[len('file://'):], 'rb')
            message = self._call_method('send' + telegram_type,
                                        params={'chat_id': chat_id}, files={telegram_type.lower(): file})
        else:
            message = self._call_method('send' + telegram_type,
                                        params={'chat_id': chat_id, telegram_type.lower(): attachment.url}, files={})

        file_id = message['result'][telegram_type.lower()][0]['file_id']

        attachment.cache(file_id, self)

    def listen(self):
        offset = None
        while True:
            params = {'timeout': self._timeout}
            if offset is not None:
                params.update({'offset': offset})
            result = self._call_method('getUpdates', params=params, files={})

            for update in result['result']:
                offset = max(offset if offset else 0, update['update_id']) + 1

                yield User(update['message']['chat']['id'], self), Message(update['message']['text'], None)

    def send_message(self, user, message):
        self._call_method('sendMessage', params={'chat_id': user.user_id, 'text': message.text}, files={})
        for attachment in message.attachments:
            self._send_attachment(user.user_id, attachment)

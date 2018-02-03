import json
from io import BufferedReader
from queue import Queue

import requests

from botal.messengesrs.messenger import Messenger
from botal.message import Message


class Telegram(Messenger):
    def __init__(self, token, timeout=10):
        self._api_url = 'https://api.telegram.org/bot{}'.format(token)
        self._timeout = timeout
        self._cached_uploads = {}
        self._messages = Queue()

    def _send_attachment(self, chat_id, attachment):
        if attachment.url in self._cached_uploads and attachment.cache:
            return self._cached_uploads[attachment.url]

        telegram_type = {
            'image': 'Photo',
            'video': 'Video',
            'audio': 'Audio',
            'application': 'Document'
        }[attachment.file_type]
        type_lower = telegram_type.lower()

        if attachment.cached_value is not None:
            message = self.call('send' + telegram_type, **{'chat_id': chat_id, type_lower: attachment.cached_value})
        elif attachment.url.startswith('file://'):
            file = open(attachment.url[len('file://'):], 'rb')
            message = self.call('send' + telegram_type, **{'chat_id': chat_id, type_lower: file})
        else:
            message = self.call('send' + telegram_type, **{'chat_id': chat_id, type_lower: attachment.url})
        file_id = message['result'][telegram_type.lower()][0]['file_id']

        attachment.cache(file_id)

    def call(self, name, **kwargs):
        files = {}
        new_params = {}
        for key, value in kwargs.items():
            if isinstance(value, BufferedReader):
                files[key] = value
            else:
                new_params[key] = value
        method_url = self._api_url + '/{}'.format(name)
        result = requests.post(method_url, params=new_params, files=files)
        parsed = json.loads(result.text)
        return parsed

    def listen(self):
        offset = None
        while True:
            params = {'timeout': self._timeout}
            if offset is not None:
                params.update({'offset': offset})
            result = self.call('getUpdates', **params)
            for update in result['result']:
                offset = max(offset if offset else 0, update['update_id']) + 1

                yield update['message']['chat']['id'], Message(update['message']['text'], None)

    def send(self, user_id, message):
        self.call('sendMessage', chat_id=user_id, text=message.text)
        for attachment in message.attachments:
            self._send_attachment(user_id, attachment)
        return message

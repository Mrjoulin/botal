import json
from io import BufferedReader

import requests

from botal.message import Message
from botal.messengesrs.messenger import IMessenger


class TelegramMessenger(IMessenger):
    API_URL = 'https://api.telegram.org/bot{}'
    DEFAULT_TIMEOUT = 10

    def __init__(self, token, timeout=None):
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        self._api_url = self.API_URL.format(token)
        self._timeout = timeout

    def _send_attachment(self, chat_id, attachment):
        if attachment.is_cached():
            return attachment.cached_value

        telegram_type = {
            'image': 'Photo',
            'video': 'Video',
            'audio': 'Audio',
            'application': 'Document'
        }[attachment.file_type]

        if attachment.is_cached():
            value = attachment.cached
        elif attachment.url.startswith('file://'):
            value = open(attachment.url[len('file://'):], 'rb')
        else:
            value = attachment.url

        message = self.call('send' + telegram_type, **{'chat_id': chat_id, telegram_type.lower(): value})

        file_id = message['result'][telegram_type.lower()][0]['file_id']

        attachment.cached = file_id

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

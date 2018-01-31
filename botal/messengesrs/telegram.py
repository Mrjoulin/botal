import json

import requests

from botal.datatypes import Message, UserInfo
from botal.messengesrs.messenger import Messenger


class Telegram(Messenger):
    def __init__(self, token, timeout=10):
        self._api_url = 'https://api.telegram.org/bot{}'.format(token)
        self._timeout = timeout

    def _call_method(self, method, **kwargs):
        method_url = self._api_url + '/{}'.format(method)
        for key, value in kwargs.items():
            if not method_url.endswith('&'):
                method_url += '?'
            method_url += '{}={}&'.format(key, value)
        result = requests.get(method_url)
        parsed = json.loads(result.text)
        return parsed

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
        method_url = self._api_url + '/sendMessage?chat_id={}&text={}'.format(user_id, text)
        requests.get(method_url)

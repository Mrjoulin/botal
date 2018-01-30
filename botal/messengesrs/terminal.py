from botal.datatypes import Message, UserInfo
from botal.messengesrs.messenger import Messenger


class Terminal(Messenger):
    def __init__(self, user_id=None):
        self.user_id = user_id

    def listen(self):
        while True:
            yield Message(input(), None), UserInfo(self.user_id, self)

    def send_message(self, user_id, text, attachments):
        print(text)

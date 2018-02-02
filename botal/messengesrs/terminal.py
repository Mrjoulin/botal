from botal.datatypes import Message, User
from botal.messengesrs.messenger import Messenger


class Terminal(Messenger):
    def __init__(self, user_id=-1):
        self.user_id = user_id

    def listen(self):
        while True:
            yield User(self.user_id, self), Message(input(), None)

    def send_message(self, user, message):
        print(message.text)

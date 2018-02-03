from botal.message import Message
from botal.messengesrs.messenger import Messenger


class Terminal(Messenger):
    def __init__(self, user_id=-1):
        self.user_id = user_id

    def listen(self):
        while True:
            yield self.user_id, Message(input(), None)

    def call(self, name, **kwargs):
        raise NotImplementedError

    def send(self, user_id, message):
        print(message.text, message.attachments)
        return message

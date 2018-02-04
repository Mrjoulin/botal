from botal.message import Message
from botal.messengesrs.messenger import Messenger


class Terminal(Messenger):
    DEFAULT_USER_ID = -1
    ATTACHMENT_PATTERN = "Attachment: url='{url}', use_cached={_use_cached}, mime='{file_type}/{file_ext}'"

    def __init__(self, user_id=None):
        if user_id is None:
            user_id = self.DEFAULT_USER_ID

        self.user_id = user_id

    def listen(self):
        while True:
            yield self.user_id, Message(input(), None)

    def call(self, name, **kwargs):
        raise NotImplementedError

    def send(self, user_id, message):
        print(message.text)
        for attachment in message.attachments:
            print(self.ATTACHMENT_PATTERN.format(**attachment.__dict__))
        return message

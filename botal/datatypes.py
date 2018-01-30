class Message:
    def __init__(self, text, attachments):
        self.attachments = attachments
        self.text = text


class UserInfo:
    def __init__(self, user_id, messenger):
        self.user_id = user_id
        self.messenger = messenger

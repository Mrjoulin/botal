class Message:
    def __init__(self, text, attachments=None):
        if attachments is None:
            attachments = []

        self.attachments = attachments
        self.text = text


class User:
    def __init__(self, user_id, messenger):
        self.user_id = user_id
        self.messenger = messenger

    def __hash__(self):
        return self.user_id * hash(self.messenger)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def send(self, message):
        self.messenger.send_message(self, message)

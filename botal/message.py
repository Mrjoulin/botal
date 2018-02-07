class Message:
    def __init__(self, text, attachments=None):
        if attachments is None:
            attachments = []

        self.attachments = attachments
        self.text = text

        self.uuid = None

    def save_message_info(self, message_id, messenger):
        self.uuid = MessageUUID(message_id, messenger)


class MessageUUID:
    def __init__(self, message_id, messenger):
        self.message_id = message_id
        self.messenger = messenger

    def __hash__(self):
        return hash(self.message_id) * hash(self.messenger)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Message:
    def __init__(self, text, attachments=None):
        if attachments is None:
            attachments = []

        self.attachments = attachments
        self.text = text

        self._sent_message_data = property()
        self._sent = False

    @property
    def sent_message_data(self):
        return self._sent_message_data

    @sent_message_data.setter
    def sent_message_data(self, value):
        if self._sent_message_data is not None:
            raise Exception('Message have already sent')

        if not isinstance(value, SentMessageData):
            raise Exception('sent_message_data must be an instance of SentMessageData class')

        self._sent = True
        self._sent_message_data = value

    @sent_message_data.getter
    def sent_message_data(self):
        if self._sent_message_data is not None:
            raise Exception("Message haven't already sent")

        return self._sent_message_data

    @sent_message_data.deleter
    def sent_message_data(self):
        self._sent_message_data = property()
        self._sent = False


class SentMessageData:
    def __init__(self, message_id, messenger):
        self.message_id = message_id
        self.messenger = messenger

    def __hash__(self):
        return hash(self.message_id) * hash(self.messenger)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

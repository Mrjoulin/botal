class Message:
    def __init__(self, text, attachments=None, message_id=None):
        if attachments is None:
            attachments = []

        self.attachments = attachments
        self.text = text
        self.message_id = message_id

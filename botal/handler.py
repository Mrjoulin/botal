from queue import Queue
from threading import Thread

from botal.datatypes import Message


class Handler:
    def __init__(self, messengers):
        self._message_handler = None
        self._mappings = {}

        self.messengers = messengers

    def _listen(self):
        queue = Queue()

        def listen_messenger(messenger_):
            for user, message in messenger_.listen():
                queue.put((user, message))

        for messenger in self.messengers:
            Thread(target=listen_messenger, args=[messenger], daemon=True).start()

        while 1:
            yield queue.get()

    def _handle_message(self, user, message):
        if user in self._mappings:
            message_handler = self._mappings[user]
        else:
            message_handler = self._message_handler(user)
            next(message_handler)

        message = Message(message.text, attachments=message.attachments)

        message_handler.send(message)
        self._mappings[user] = message_handler

    def handler(self, func):
        self._message_handler = func
        return func

    def run_handler(self):
        def handle():
            for user, message in self._listen():
                Thread(target=self._handle_message, args=[user, message], daemon=True).start()

        Thread(target=handle).run()

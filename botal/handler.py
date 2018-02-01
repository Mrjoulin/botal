from queue import Queue
from threading import Thread

from botal.datatypes import Message, UserInfo


class Handler:
    def __init__(self, messengers):
        self._message_handler = None

        self.messengers = messengers
        self.mappings = {}

    def _listen(self):
        queue = Queue()

        def listen_messenger(messenger_):
            for message in messenger_.listen():
                queue.put(message)

        for messenger in self.messengers:
            Thread(target=listen_messenger, args=[messenger], daemon=True).start()

        while 1:
            yield queue.get()

    def _handle_message(self, message, user_info):
        if user_info.user_id in self.mappings.keys():
            message_handler = self.mappings[user_info.user_id]
        else:
            message_handler = self._message_handler(user_info)
            next(message_handler)

        message = Message(text=message.text, attachments=message.attachments)
        result = message_handler.send(message)

        if result is None:
            return

        if isinstance(result, (list, tuple)) and len(result) == 2:
            answer, attachments = result
            if answer is None:
                answer = ''
        else:
            answer, attachments = result, []

        user_info.messenger.send_message(user_info.user_id, answer, attachments)

    def handler(self):
        def decorator(func):
            self._message_handler = func
            return func

        return decorator

    def run_handler(self):
        def handle():
            for message, user_info in self._listen():
                Thread(target=self._handle_message, args=[message, user_info], daemon=True).start()

        Thread(target=handle).run()

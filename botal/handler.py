from threading import Thread

from botal.user import User


class Handler:
    def __init__(self, messenger):
        self._message_handler = None
        self._mappings = {}

        self.messenger = messenger

    def _listen(self):
        for user_id, message in self.messenger.listen():
            yield user_id, message

    def _handle_message(self, user_id, message):
        if user_id in self._mappings:
            user = self._mappings[user_id]
        else:
            user = User(user_id, self._message_handler)
            self._mappings[user_id] = user
        user.handle(message)

    def handler(self, func):
        self._message_handler = func
        return func

    def run_handler(self):
        def handle():
            for user_id, message in self._listen():
                Thread(target=self._handle_message, args=[user_id, message], daemon=True).start()

        Thread(target=handle).run()

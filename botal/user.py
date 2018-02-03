from threading import Lock


class User:
    def __init__(self, user_id, handler):
        self.user_id = user_id

        self._lock = Lock()
        self._handler = handler(user_id)
        next(self._handler)

    def handle(self, message):
        with self._lock:
            self._handler.send(message)

    def __hash__(self):
        return self.user_id

    def __eq__(self, other):
        return self.user_id == other.user_id

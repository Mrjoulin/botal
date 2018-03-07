from threading import Thread, Lock


class Botal:
    class _ThreadSafeGenerator:
        def __init__(self, uuid, handler):
            self.uuid = uuid

            self._lock = Lock()
            self._handler = handler(uuid)
            next(self._handler)

        def send(self, message):
            with self._lock:
                self._handler.send(message)

        def __hash__(self):
            return self.uuid

        def __eq__(self, other):
            return self.uuid == other.user_id

    def __init__(self, generator, uuid):
        self._message_handler = None
        self._mappings = {}

        self.generator = generator
        self.uuid = uuid

    def _handle_message(self, user_id, message):
        if user_id in self._mappings:
            user = self._mappings[user_id]
        else:
            user = self._ThreadSafeGenerator(user_id, self._message_handler)
            self._mappings[user_id] = user
        user.send(message)

    def handler(self, func):
        self._message_handler = func
        return func

    def run(self):
        def handle():
            for event in self.generator:
                uuid = self.uuid(event)
                Thread(target=self._handle_message, args=[uuid, event], daemon=True).start()

        thread = Thread(target=handle, daemon=True)
        thread.start()
        thread.join()

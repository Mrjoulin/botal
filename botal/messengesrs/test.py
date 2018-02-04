from queue import Queue

from botal.message import Message
from botal.messengesrs import IMessenger


class TestMessenger(IMessenger):
    def __init__(self):
        self._input = Queue()
        self._output = Queue()
        self._user_id = 0

    def call(self, name, **kwargs):
        raise NotImplementedError

    def listen(self):
        while True:
            yield self._user_id, Message(self._input.get())

    def send(self, user_id, message):
        self._output.put(message)

    def output_on(self, message):
        assert self._input.empty()
        self._input.put(message)
        return self._output.get()

    def restart(self):
        self._output = Queue()
        self._user_id += 1

from abc import ABCMeta, abstractmethod


class Messenger(metaclass=ABCMeta):
    # Check new messages and return if exists
    @abstractmethod
    def listen(self):
        pass

    # Send message to user
    @abstractmethod
    def send_message(self, user, message):
        pass

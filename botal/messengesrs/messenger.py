from abc import ABCMeta, abstractmethod


class Messenger(metaclass=ABCMeta):
    # Call API method
    @abstractmethod
    def call(self, name, **kwargs):
        raise NotImplementedError

    # Check new messages and return if exists
    @abstractmethod
    def listen(self):
        raise NotImplementedError

    # Send message to user
    @abstractmethod
    def send(self, user_id, message):
        raise NotImplementedError

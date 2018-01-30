import vk_api
from vk_api import longpoll
from vk_api.longpoll import VkEventType

from botal.datatypes import Message, UserInfo
from botal.messengesrs.messenger import Messenger


class Vk(Messenger):
    def __init__(self, login=None, password=None, token=None):
        self.sess = vk_api.VkApi(login=login, password=password, token=token)
        if not token:
            self.sess.auth()

        self.api = self.sess.get_api()
        self.lp = longpoll.VkLongPoll(self.sess)

    def listen(self):
        for event in self.lp.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                yield Message(event.text, event.attachments), UserInfo(event.user_id, self)

    def send_message(self, user_id, text, attachments):
        self.api.messages.send(user_id=user_id, message=text, attachments=attachments)

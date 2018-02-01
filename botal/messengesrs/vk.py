import re
import urllib.request
from os import remove

import vk_api
from vk_api import longpoll, VkUpload
from vk_api.longpoll import VkEventType

from botal.datatypes import Message, UserInfo
from botal.messengesrs.messenger import Messenger


class Vk(Messenger):
    def __init__(self, login=None, password=None, token=None):
        self.sess = vk_api.VkApi(login=login, password=password, token=token)
        if not token:
            self.sess.auth()

        self.api = self.sess.get_api()
        self.upload = VkUpload(self.sess)
        self.lp = longpoll.VkLongPoll(self.sess)

    def _upload_attachment(self, attachment):
        if attachment.url.startswith('https://vk.com/'):
            result = re.findall('(photo|video|audio|doc|wall|market)(-?\d+)_(\d+)', attachment.url)[0]
            return '{}{}_{}'.format(*result)

        cached = attachment.get_cached(self)
        if cached is not None:
            return cached

        upload_methods = {
            'image': ('photo', lambda x: self.upload.photo_messages([x])),
            'video': ('video', lambda x: self.upload.video(video_file=x)),
            'audio': ('audio', lambda x: self.upload.audio_message(x)),
            'application': ('document', lambda x: self.upload.document(x))
        }

        vk_type, upload_method = upload_methods[attachment.file_type]
        if attachment.url.startswith('file://'):
            uploaded = upload_method(attachment.url[len('file://'):])[0]
        else:
            filename = '.botaltmp.' + attachment.file_ext
            urllib.request.urlretrieve(attachment.url, filename)
            try:
                uploaded = upload_method(filename)[0]
            finally:
                remove(filename)

        vk_attachment = '{}{}_{}'.format(vk_type, uploaded['owner_id'], uploaded['id'])
        attachment.cache(vk_attachment, self)
        return vk_attachment

    def listen(self):
        for event in self.lp.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                yield Message(event.text, event.attachments), UserInfo(event.user_id, self)

    def send_message(self, user_id, text, attachments):
        to_upload = []
        for attachment in attachments:
            to_upload.append(attachment)
        attachments = []
        for url in to_upload:
            attachments.append(self._upload_attachment(url))

        self.api.messages.send(user_id=user_id, message=text, attachment=','.join(attachments))

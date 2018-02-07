import re
import urllib.request
from os import remove

import vk_api
from vk_api import longpoll, VkUpload
from vk_api.longpoll import VkEventType

from botal.message import Message, SentMessageData
from botal.messengesrs.messenger import IMessenger


class VkMessenger(IMessenger):
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

        if attachment.is_cached():
            return attachment.cached

        upload_methods = {
            'image': ('photo', lambda x: self.upload.photo_messages([x])),
            'video': ('video', lambda x: self.upload.video(video_file=x)),
            'audio': ('audio', lambda x: self.upload.audio_message(x)),
            'application': ('document', lambda x: self.upload.document(x))
        }

        vk_type, upload_method = upload_methods[attachment.file_type]
        if attachment.is_file():
            uploaded = upload_method(attachment.url[len('file://'):])[0]
        else:
            filename = '.botaltmp.' + attachment.file_ext
            urllib.request.urlretrieve(attachment.url, filename)
            try:
                uploaded = upload_method(filename)[0]
            finally:
                remove(filename)

        vk_attachment = '{}{}_{}'.format(vk_type, uploaded['owner_id'], uploaded['id'])
        attachment.cached = vk_attachment
        return vk_attachment

    def listen(self):
        for event in self.lp.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                message = Message(event.text, attachments=event.attachments)
                message.sent_message_data = SentMessageData(event.user_id, self)

                yield event.user_id, message

    def call(self, name, **kwargs):
        self.sess.method(name, values=kwargs)

    def send(self, user_id, message):
        to_upload = []
        forward_messages_id = []
        for attachment in message.attachments:
            if isinstance(attachment, Message):
                forward_messages_id.append(attachment.sent_message_data.message_id)
            else:
                to_upload.append(attachment)
        attachments = []

        for url in to_upload:
            attachments.append(self._upload_attachment(url))
        message_id = self.api.messages.send(user_id=user_id,
                                            message=message.text,
                                            attachment=','.join(attachments),
                                            forward_messages=','.join(map(str, forward_messages_id)))
        message.sent_message_data = SentMessageData(message_id, self)
        return message

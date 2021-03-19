from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.exceptions import ApiError
from vk_api.vk_api import VkApiGroup
from vk_api.upload import VkUpload
import requests
import logging
import time


from .botal import Botal


DEFAULT_EVENTS = [VkBotEventType.MESSAGE_NEW]


class VkBot(Botal):
    def __init__(self, token=None, tokens=None, events=None):
        if token is None and tokens is None:
            logging.error("No tokens given")
            return

        self.tokens = []

        self.group_id = None
        self.sess = None
        self.uploads = []
        # Uploads: [
        #   {
        #       "object": <VkUpload object>,
        #       "last_usage": <timestamp of last object usage>
        #   }
        # ]
        self.api_methods = []
        # API methods: [
        #   {
        #       "object": <VkApiMethod object>,
        #       "last_usage": <timestamp of last object usage>
        #   }
        # ]

        success = self.load_tokens(tokens if tokens else [token])

        if not success:
            logging.error("No tokens loaded")
            return

        self.lp = VkBotLongPoll(self.sess, group_id=self.group_id)

        self.events = events or DEFAULT_EVENTS

        super(VkBot, self).__init__(self.generator(), uuid)

    def load_tokens(self, tokens):
        loaded_tokens = 0
        for token in tokens:
            success = self.add_token(token)

            if success:
                loaded_tokens += 1

        logging.info("Successful load %s/%s tokens" % (loaded_tokens, len(tokens)))

        return bool(loaded_tokens)

    def add_token(self, token):
        if not isinstance(token, str) or not len(token):
            logging.error("Invalid token format: %s" % token)
            return False

        if token in self.tokens:
            logging.error("Token has already been added earlier: %s" % token)
            return False

        def get_object_dict(obj):
            return {
                "object": obj,
                "last_usage": time.time()
            }

        sess = VkApiGroup(token=token)
        upload = VkUpload(sess)
        api = sess.get_api()

        # Check API method
        group_id = get_group_id(api)

        if group_id is not None and (self.group_id is None or self.group_id == group_id):
            self.sess = self.sess or sess
            self.uploads.append(get_object_dict(upload))
            self.api_methods.append(get_object_dict(api))

            self.group_id = group_id

            return True
        elif group_id is None:
            logging.error("Unable to connect API token: %s" % token)
        else:
            logging.error("API token given from another group: %s" % token)

        return False

    def generator(self):
        return filter(
            lambda x: x.type in self.events, safe_listen(self.lp)
        )

    def get_api(self):
        return self.get_object(self.api_methods)

    def get_upload(self):
        return self.get_object(self.uploads)

    def get_object(self, objects_list):
        # Find the oldest object usage
        last_usages = list(map(lambda api: api["last_usage"], objects_list))
        api_index = last_usages.index(min(last_usages))
        # Update object usage time
        objects_list[api_index]["last_usage"] = time.time()
        # Return object
        return objects_list[api_index]["object"]

    # To call API methods just: bot.messages.send(...)
    def __getattr__(self, method):
        return self.get_api().__getattr__(method)


def uuid(x):
    return x.obj.message['peer_id']


def safe_listen(lp):
    while True:
        try:
            yield from lp.listen()
        except Exception as e:
            if isinstance(e, ApiError):
                logging.error(e)

            if not isinstance(e, requests.exceptions.ReadTimeout) and \
                    not isinstance(e, requests.exceptions.ConnectionError):
                logging.error(str(e))


def get_group_id(api):
    try:
        group_info = api.groups.getById()[0]

        return group_info["id"]
    except Exception as e:
        logging.exception(e)

        return None

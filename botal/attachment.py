import mimetypes


class Attachment:
    _cached = {}

    def __init__(self, url, cache=True):
        self.url = url
        self.file_type, self.file_ext = mimetypes.guess_type(url)[0].split('/')

        self._cache = cache

    def cache(self, value, messenger):
        if self._cache:
            if messenger.__class__.__name__ not in self._cached:
                self._cached[messenger.__class__.__name__] = {}
            self._cached[messenger.__class__.__name__][self.url] = value

    def get_cached(self, messenger):
        messenger_cache = self._cached.get(messenger)
        if not messenger_cache:
            return None
        return messenger_cache.get(self.url)

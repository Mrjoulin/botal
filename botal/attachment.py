import mimetypes


class Attachment:
    _cached = {}

    def __init__(self, url, cache=True):
        self.url = url
        self.file_type, self.file_ext = mimetypes.guess_type(url)[0].split('/')

        if cache:
            self.cached_value = self._cached.get(self.url)
        else:
            self.cached_value = None

    def cache(self, value):
        self._cached[self.url] = value

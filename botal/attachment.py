import mimetypes


class Attachment:
    _cached = {}

    def __init__(self, url, use_cached=True):
        self.url = url
        self.file_type, self.file_ext = mimetypes.guess_type(url)[0].split('/')
        self._use_cached = use_cached

    def is_file(self):
        return self.url.startswith('file://')

    def is_cached(self):
        return self._use_cached and self.url in self._cached

    @property
    def cached(self):
        if self._use_cached:
            return self._cached[self.url]
        else:
            return None

    @cached.setter
    def cached(self, value):
        self._cached[self.url] = value

    @cached.deleter
    def cached(self):
        del self._cached[self.url]

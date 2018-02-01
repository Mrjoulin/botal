import mimetypes


class Attachment:
    def __init__(self, url, cache=True):
        self.url = url
        self.file_type, self.file_ext = mimetypes.guess_type(url)[0].split('/')
        self.cache = cache

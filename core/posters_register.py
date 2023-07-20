import os

from .exceptions import MeteoSangueException


class PostersRegister():

    def __init__(self):
        self._posters = []

    def register_poster(self, poster, log_attribute):
        self._posters.append((poster, log_attribute))

    def get_posters(self):
        return self._posters

    def run(self, status, log):
        for poster in self._posters:
            if log and not getattr(log, poster[1], False):
                try:
                    image_path = log.image.name if os.path.exists(log.image.name) else None
                    poster[0](status, image_path)
                    setattr(log, poster[1], True)
                except MeteoSangueException as ex:
                    print (ex)


posters_register = PostersRegister()
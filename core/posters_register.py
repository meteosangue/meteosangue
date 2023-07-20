import os

from .exceptions import MeteoSangueException


class PostersRegister():

    def __init__(self):
        self._posters = []

    def register_poster(self, poster, log_attribute):
        self._posters.append((poster, log_attribute))

    def get_posters(self):
        return self._posters

    def run(self, status, image_path):
        for poster in self._posters:
            try:
                poster[0](status, image_path)
            except MeteoSangueException as ex:
                print (ex)


posters_register = PostersRegister()
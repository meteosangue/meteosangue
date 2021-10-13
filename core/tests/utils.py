import os
import shutil


class MockPhantomJS():

    def __init__(self, content, wrong_save=False):
        self._content = content
        self._wrong_save = wrong_save

    @property
    def page_source(self):
        return self._content

    def implicitly_wait(self, wait):
        pass

    def set_window_size(self, w, h):
        pass

    def get(self, url):
        pass

    def save_screenshot(self, file_path):
        shutil.copy(
            os.path.join(
                os.path.dirname(__file__), 
                'data', 
                'meteo_fake_upload.png' if not self._wrong_save else 'meteo_wrong_upload.png'
            ), 
            file_path
        )

    def quit(self):
        pass

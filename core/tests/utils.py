class MockPhantomJS():

    def __init__(self, content):
        self._content = content

    @property
    def page_source(self):
        return self._content

    def set_window_size(self, w, h):
        pass

    def get(self, url):
        pass

    def save_screenshot(self,file_path):
        pass

    def quit(self):
        pass
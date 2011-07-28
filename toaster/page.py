
from toaster.convertible import Convertible

class Page(Convertible):
    
    def __init__(self, path):
        self.read_yaml(path)
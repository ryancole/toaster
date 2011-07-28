
import os, re, yaml
from toaster.convertible import Convertible


class Page(Convertible):
    
    def __init__(self, site, path):
        self.site = site
        self.path = path
        self.filename = os.path.basename(path)
        self.process(self.filename)
        

    def process(self, filename):
        self.url = os.path.join(self.site.settings['destination'], self.path)
        self.meta, self.content = self.read_yaml(self.path)
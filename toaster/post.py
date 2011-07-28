
import os, re, datetime, markdown
from toaster.convertible import Convertible


class Post(Convertible):
    
    def __init__(self, site, path):
        self.site = site
        self.path = path
        self.filename = os.path.basename(path)
        self.process(self.filename)
        

    def process(self, filename):
        
        # check the filename for appropriate syntax
        groups = re.match('(.+\/)*(\d+-\d+-\d+)-(.*)(\.[^.]+)$', filename)
        if groups:
            
            # parse filename data
            self.date = datetime.datetime.strptime(groups.group(2), '%Y-%m-%d')
            self.slug = groups.group(3).lower()
            self.extension = groups.group(4).lower()
            self.url = os.path.join(os.path.relpath(self.site.settings['destination']),
                                    str(self.date.year), str(self.date.month),
                                    str(self.date.day), '%s.html' % self.slug)
            
            # read in the yaml front matter and post content
            self.meta, content = self.read_yaml(self.path)
            
            # store the post content as markdown
            self.content = markdown.markdown(content)
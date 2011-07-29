import os, yaml, jinja2, shutil, datetime

from toaster.post import Post
from toaster.page import Page


class Site:
    
    def __init__(self):
        
        # some site variables
        self.timestamp = datetime.datetime.now()
        
        # initialize the default settings
        self.settings = { 'source': os.getcwd(), 'destination': os.path.join(os.getcwd(), '_site') }
        
        # load settings from the config file
        self.load_settings(os.path.join(self.settings['source'], '_config.yml'))
        
        # initialize the jinja template environment
        template_loader = jinja2.FileSystemLoader(os.path.join(self.settings['source'], '_layouts'))
        self.template_environment = jinja2.Environment(loader=template_loader)
        
    
    def load_settings(self, path):
        with open(path) as stream:
            self.config = path
            self.settings.update(yaml.load(stream))
        
    
    def process(self):
        
        # read in the posts
        posts_path = os.path.join(self.settings['source'], '_posts')
        self.posts = [Post(self, os.path.join(posts_path, filename)) for filename in os.listdir(posts_path)]
        
        self.pages = list()
        
        # read in the pages and static content
        for directory, directories, filenames in os.walk(self.settings['source']):
            
            # filter out directories that contain toaster content
            for dir in directories:
                if os.path.relpath(dir).startswith(('_', '.')):
                    directories.remove(dir)
            
            # if the current directory contains toast content then skip it, too
            if os.path.relpath(directory).startswith('_'):
                continue
            
            if filenames:
                for filename in filenames:
                    
                    # filter out files that contain toaster content
                    if filename.startswith(('.', '_')):
                        continue
                    
                    with open(os.path.join(directory, filename)) as stream:
                        first_three = stream.read(3)
                    
                    # treat the file as a page if it has yaml front matter
                    if first_three == '---':
                        self.pages.append(Page(self, os.path.join(directory, filename)))
                        
                    else:
                        base_path = os.path.relpath(os.path.join(self.settings['destination'], os.path.relpath(directory)))
                        if not os.path.exists(base_path):
                            os.makedirs(base_path)
                        
                        shutil.copy(os.path.join(directory, filename), base_path)
    
    
    def render(self):
        for post in self.posts:
            post.render()
        
        for page in self.pages:
            page.render()
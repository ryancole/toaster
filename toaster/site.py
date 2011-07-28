
import os, yaml, jinja2
from toaster.post import Post

class Site:
    
    def __init__(self):
        
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
        
        # read in the pages and static content
        for directory, directories, filenames in os.walk(self.settings['source']):
            if filenames:
                print filenames
    
    
    def render(self):
        for post in self.posts:
            post.render()
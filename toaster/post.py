
import yaml, re, jinja2, markdown

class Post:

    def __init__(self, settings, path):
        self.path = path
        self.settings = settings
        self.front_matter, self.content = self.parse(path)


    def parse(self, path):
        
        # extract the yaml front matter and post content
        with open(path) as stream:
            match_result = re.match('---\n(.*?)\n---\n(.*)', stream.read(), re.S)
        
        # provide front matter if available
        if match_result:
            return yaml.load(match_result.group(1)), match_result.group(2)
        
        # otherwise nothing
        return None, None
    
    
    def toast(self):
        
        # instanciate the template environment
        template_loader = jinja2.FileSystemLoader(self.settings['layouts'])
        template_environment = jinja2.Environment(loader=template_loader)
        
        

import yaml, re, jinja2, markdown, datetime, os


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
    
    
    def toast(self, converter):
        
        # instanciate the template environment
        template_loader = jinja2.FileSystemLoader(self.settings['layouts'])
        template_environment = jinja2.Environment(loader=template_loader)
        
        # template context
        template_context = dict(content=converter.convert(self.content),
                                meta=self.front_matter)
        
        # get the desired template file from the environment
        template = template_environment.get_template('%s.html' % self.front_matter['layout'])
        
        # get the post's date from the name
        filename = os.path.splitext(os.path.basename(self.path))[0].split('-')
        date = datetime.date(int(filename[0]), int(filename[1]), int(filename[2]))
        filename = '%s.html' % '-'.join(filename[3:]).lower()
        
        # create the base path if it does not exist
        filepath = os.path.join(self.settings['destination'], str(date.year), str(date.month), str(date.day))
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        
        # write the rendered post to disk
        with open(os.path.join(filepath, filename), 'w') as stream:
            stream.writelines(template.render(template_context))
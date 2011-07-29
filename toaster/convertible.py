
import os, re, yaml


class Convertible:
    
    def read_yaml(self, path):
        """ read the yaml front matter """
        
        with open(path) as stream:
            content = stream.read()
            
        groups = re.match('---\s+(.*?)\s+---\s+(.*)', content, re.S)
        if groups:
            return (yaml.load(groups.group(1)), groups.group(2))
        
        return (None, None)
    
    
    def render(self):
        
        # populate template context hash
        template_context = { 'site': self.site, 'meta': self.meta, 'content': self.content }
        
        # get the desired template file from the environment
        template = self.site.template_environment.get_template('%s.html' % self.meta['layout'])
        
        # create the base path if it does not exist
        if not os.path.exists(os.path.dirname(self.url)):
            os.makedirs(os.path.dirname(self.url))
        
        # write the rendered post to disk
        with open(self.url, 'w') as stream:
            stream.writelines(template.render(template_context))
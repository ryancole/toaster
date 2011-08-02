# -*- coding: utf-8 -*-

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
        
        # get the desired template file from the environment
        template = self.site.template_environment.get_template('%s.html' % self.meta['layout'])
        
        # create the base path if it does not exist
        base_path = os.path.relpath(os.path.join(self.site.settings['destination'], os.path.dirname(self.url)))
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        
        # write the rendered post to disk
        with open(os.path.relpath(os.path.join(self.site.settings['destination'], self.url)), 'w') as stream:
            stream.writelines(template.render(self.context))
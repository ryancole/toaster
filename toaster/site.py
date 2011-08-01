# -*- coding: utf-8 -*-

import os, yaml, jinja2, shutil, datetime

from toaster.post import Post
from toaster.page import Page


class HtmlLoader(jinja2.BaseLoader):

    def __init__(self, paths):
        self.paths = paths
    
    
    def get_source(self, environment, template):
        
        for path in self.paths:
            for directory, directories, filenames in os.walk(path):
                
                # filter out directories that contain toaster content
                for dir in directories:
                    if os.path.relpath(dir).startswith(('_', '.')):
                        directories.remove(dir)
            
                # if the current directory contains toast content then skip it, too
                if os.path.relpath(directory).startswith('_') and os.path.relpath(directory) != '_layouts':
                    continue
                
                if os.path.isfile(os.path.join(directory, template)):
                    
                    mtime = os.path.getmtime(os.path.join(directory, template))
                    
                    def uptodate():
                        return os.path.getmtime(os.path.join(directory, template)) == mtime
                    
                    with file(os.path.join(directory, template)) as stream:
                        content = stream.read().decode('utf-8')
                    
                    return content, os.path.join(directory, template), uptodate
                
            raise jinja2.TemplateNotFound(template)


    def list_templates(self):
        
        # init templates set; ugly
        templates = set()
        
        # list html filess
        for path in self.paths:
            for directory, directories, filenames in os.walk(path):
 
                # filter out directories that contain toaster content
                for dir in directories:
                    if os.path.relpath(dir).startswith(('_', '.')):
                        directories.remove(dir)
            
                # if the current directory contains toast content then skip it, too
                if os.path.relpath(directory).startswith('_') and os.path.relpath(directory) != '_layouts':
                    continue
                
                # add files ending with an html ext
                for filename in filenames:
                    if filename.endswith('.html'):
                        templates.add(os.path.relpath(os.path.join(directory, filename)))

        return sorted(templates)


class Site:
    
    def __init__(self):
        
        # initialize the default settings
        self.settings = { 'source': os.getcwd(), 'destination': os.path.join(os.getcwd(), '_site') }
        
        # load settings from the config file
        self.load_settings(os.path.join(self.settings['source'], '_config.yml'))
        
        # initialize the jinja template environment
        self.template_environment = jinja2.Environment(loader=HtmlLoader([self.settings['source']]), autoescape=True)
    
    
    def load_settings(self, path):
        with open(path) as stream:
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
                    
                    # treat the file as a page if it's html
                    if filename.endswith('.html'):
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
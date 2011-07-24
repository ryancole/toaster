
import os, yaml, datetime, shutil
import toaster.post
import toaster.converters


class Toaster:

    def __init__(self):
        self.config = './_config.yml'
        self.converters = toaster.converters.ConverterManager()
        self.settings = dict(source='.', destination='./_site', layouts='./_layouts', posts='./_posts')


    def load_config(self, path):
        with open(path) as stream:
            self.config = path
            self.settings.update(yaml.load(stream))
        return self.settings


    def toast_directory(self, path):
        
        # walk the provided source path
        for directory, directories, filenames in os.walk(path):
            
            # skip over any no-op dirs
            if directory.startswith((self.settings['destination'], self.settings['layouts'])):
                continue
            
            # toast each file
            for filename in filenames:
                self.toast_file(os.path.join(directory, filename))


    def toast_file(self, path):
        
        # skip over any no-op files
        if os.path.basename(path) in [os.path.basename(self.config)]:
            return
        
        # operate on known converters
        basename, extension = os.path.splitext(os.path.basename(path))
        if extension in self.converters.extensions:
            
            # instantiate the post object
            post = toaster.post.Post(self.settings, path)
            
            # toast the post
            post.toast(self.converters.converter_for_extension(extension))
        
        else:
            
            # unknown markup language; simply copy
            if not os.path.exists(os.path.dirname(os.path.join(self.settings['destination'], os.path.relpath(path)))):
                os.makedirs(os.path.dirname(os.path.join(self.settings['destination'], os.path.relpath(path))))
            
            shutil.copy(path, os.path.join(self.settings['destination'], os.path.relpath(path)))
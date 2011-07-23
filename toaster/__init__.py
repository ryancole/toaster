
import os, yaml, datetime, shutil
import toaster.post

class Toaster:


    def __init__(self):
        self.config = './_config.yml'
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
        
        # operate on known markup langauges
        basename, extension = os.path.splitext(os.path.basename(path))
        if extension in ['.markdown', '.md']:
            
            # instantiate the post object
            post = toaster.post.Post(self.settings, path)
            
            # toast the post
            post.toast()
        
        else:
            
            # unknown markup language; simply copy
            if not os.path.exists(os.path.dirname(os.path.join(self.settings['destination'], os.path.relpath(path)))):
                os.makedirs(os.path.dirname(os.path.join(self.settings['destination'], os.path.relpath(path))))
            
            shutil.copy(path, os.path.join(self.settings['destination'], os.path.relpath(path)))


def render_post(template_environment, file_name, file_content, path_site):

    # parse the yaml front matter
    front_matter = yaml.load(file_content.group(1))
    
    # format the template context variable
    template_context = dict(content=markdown.markdown(file_content.group(2)),
                            title=front_matter['title'])
    
    # get the desired template file from the environment
    template = template_environment.get_template('%s.html' % front_matter['layout'])
    
    # read out the file's date
    file_name = file_name.split('-')
    file_date = datetime.date(int(file_name[0]), int(file_name[1]), int(file_name[2]))
    file_name = '-'.join(file_name[3:])
    
    # create the base path if it does not exist
    file_path = '/%s/%s/%s/%s.html' % (file_date.year, file_date.month, file_date.day, os.path.splitext(file_name)[0])
    if not os.path.exists('%s%s' % (path_site, os.path.dirname(file_path))):
        os.makedirs('%s%s' % (path_site, os.path.dirname(file_path)))
    
    # write the rendered post to disk
    with open('%s%s' % (path_site, file_path), 'w') as stream:
        stream.writelines(template.render(template_context))
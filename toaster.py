#!/usr/bin/env python

import os, jinja2, yaml, re

def render_post(template_environment, path_post, path_site):

    # read in the entire post
    with open(path_post, 'r') as stream:
        post_content = stream.read()

    # extract the yaml front matter
    front_matter = re.match('---\n(.*?)\n---', post_content, re.S)
    
    # only render files with front matter
    if not front_matter:
        return
    
    front_matter = yaml.load(front_matter.group(1))
    
    # save the rendered template to disk
    template = template_environment.get_template('%s.html' % front_matter['template'])
    
    with open('%s/%s.html' % (path_site, os.path.splitext(os.path.basename(path_post))[0]), 'w') as stream:
        stream.writelines(template.render())


if __name__ == '__main__':
    
    # get the working directory
    path_working = os.getcwd()
    
    # load the config file
    with file(os.path.join(path_working, '_config.yml')) as stream:
        config = yaml.load(stream)
    
    # initialize the template environment
    template_loader = jinja2.FileSystemLoader(os.path.join(path_working, '_templates'))
    template_environment = jinja2.Environment(loader=template_loader)
    
    # render each post
    path_site = os.path.join(path_working, '_site')
    path_posts = os.path.join(path_working, '_posts')
    for path_post in [os.path.join(path_posts, f) for f in os.listdir(path_posts)]:
        render_post(template_environment, path_post, path_site)
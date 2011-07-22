import os, jinja2, yaml, re, markdown, datetime, shutil


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


def begin():
    
    # get the working directory
    path_working = os.getcwd()

    # relative paths
    path_site = os.path.join(path_working, '_site')
    path_posts = os.path.join(path_working, '_posts')
    path_layouts = os.path.join(path_working, '_layouts')
    
    # initialize the template environment
    template_loader = jinja2.FileSystemLoader(path_layouts)
    template_environment = jinja2.Environment(loader=template_loader)
    
    for directory, directories, filenames in os.walk(path_working):
        
        # skip the data directories
        if directory.startswith((path_site, path_layouts)):
            continue
        
        # handle each file, otherwise
        for filename in filenames:
            
            # skip the config file
            if filename in ['_config.yml']:
                continue
            
            # check for a known file format
            basename, extension = os.path.splitext(filename)
            if extension in ['.markdown']:
            
                # extract the yaml front matter and post content
                with open(os.path.join(directory, filename)) as stream:
                    file_content = re.match('---\n(.*?)\n---\n(.*)', stream.read(), re.S)
                
                # if the file has front matter then render it
                if file_content:
                    render_post(template_environment, filename, file_content, path_site)
            
            else:
                
                file_path = '%s%s' % (path_site, os.path.join(directory, filename)[len(path_working):])
                
                if not os.path.exists(os.path.dirname(file_path)):
                    os.makedirs(os.path.dirname(file_path))

                # simply copy this file into the site directory
                shutil.copy(os.path.join(directory, filename), file_path)
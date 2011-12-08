import os, setuptools

README = os.path.join(os.path.dirname(__file__),'README.rst')

setuptools.setup(
    name = 'toaster',
    version = '0.0.3',
    packages = setuptools.find_packages(),
    scripts = ['bin/toast'],
    install_requires = ['pyyaml', 'markdown', 'jinja2'],
    
    # explicity include readme
    package_data = {'': ['README.rst']},
    
    # meta-data for upload to pypi
    author = 'Ryan Cole',
    author_email = 'ryan@rycole.com',
    description = 'A static blog generator inspired by Jekyll.',
    license = 'MIT',
    keywords = 'toaster static blog jekyll',
    url = 'https://github.com/ryancole/toaster',
    include_package_data = True
)
from distutils.core import setup

setup(
    name='toaster',
    version='0.0.1',
    author='Ryan Cole',
    author_email='ryan@rycole.com',
    packages=['toaster'],
    scripts=['bin/toaster.py'],
    url='http://pypi.python.org/pypi/toaster/',
    description='A static blog generator.',
    long_description=open('readme.md').read(),
)
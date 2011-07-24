import os
from setuptools import setup, find_packages

README = os.path.join(os.path.dirname(__file__),'README.rst')
long_description = open(README).read() + '\n'

setup(name='toaster',
      version='0.0.1',
      description='A static blog generator inspired by Jekyll.',
      long_description=long_description,
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
      ],
      keywords='toaster pip easy_install distutils setuptools',
      author='Ryan Cole',
      author_email='ryan@rycole.com',
      url='https://github.com/ryancole/toaster',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
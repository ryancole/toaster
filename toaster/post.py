# -*- coding: utf-8 -*-

import os, re, datetime, markdown

from toaster.convertible import Convertible
from toaster.converters import ConverterProvider
from toaster.converters import *


class Post(Convertible):
    
    def __init__(self, site, path):
        
        # store post path data
        self.site = site
        self.path = path
        self.filename = os.path.basename(path)
        
        # process data from post file
        self.process(self.filename)
        

    def __repr__(self):
        return self.meta['title']


    def process(self, filename):
        
        # check the filename for appropriate syntax
        groups = re.match('(.+\/)*(\d+-\d+-\d+)-(.*)(\.[^.]+)$', filename)
        if groups:
            
            # read in the yaml front matter and post content
            self.meta, content = self.read_yaml(self.path)
            
            # parse filename data
            self.date = datetime.datetime.strptime(groups.group(2), '%Y-%m-%d')
            self.slug = groups.group(3).lower()
            self.extension = groups.group(4).lower()
            self.url = os.path.join(str(self.date.year), str(self.date.month),
                                    str(self.date.day), '%s.html' % self.slug)
            
            # store the post content as converted markup
            for converter in ConverterProvider.plugins:
                converter = converter()
                if self.extension in converter.extensions:
                    self.content = converter.convert(content)
                    break
                
                else:
                    # no converter found for this extensions; fall back to raw
                    self.content = content
            
            # format the template context
            self.context = { 'title': self.meta['title'], 'date': self.date,
                             'url': self.url, 'content': self.content }
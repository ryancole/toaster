# -*- coding: utf-8 -*-

import markdown

from toaster.converters import ConverterProvider


class MarkdownConverter(ConverterProvider):
    
    def __init__(self):
        self.extensions = ['.md', '.markdown']
    
    def convert(self, content):
        return markdown.markdown(content)
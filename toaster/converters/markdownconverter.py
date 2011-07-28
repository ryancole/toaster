from toaster.converters import ConverterProvider
from markdown import markdown

class MarkdownConverter(ConverterProvider):
    
    def __init__(self):
        self.extensions = ['.md', '.markdown']
    
    def convert(self, content):
        return markdown(content)
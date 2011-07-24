
from toaster.converters import markdown

class ConverterManager:
    
    def __init__(self):
        self.converters = dict(markdown=markdown.MarkdownConverter())
        self.extensions = [converter.extensions for converter in self.converters.values()]
        self.extensions = sum(self.extensions, [])
    
    def converter_for_extension(self, extension):
        for converter in self.converters.keys():
            if extension in self.converters[converter].extensions:
                return self.converters[converter]
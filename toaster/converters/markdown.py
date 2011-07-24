
import markdown as _markdown

class MarkdownConverter:
    
    def __init__(self):
        self.extensions = ['.md', '.markdown']
    
    def convert(self, content):
        return _markdown.markdown(content)
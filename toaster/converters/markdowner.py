
import markdown

class MarkdownConverter:
    
    def __init__(self):
        self.extensions = ['.md', '.markdown']
    
    def convert(self, content):
        return markdown.markdown(content)
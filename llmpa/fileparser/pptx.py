from .base import BaseFileParser


class PptxFileParser(BaseFileParser):
    def __init__(self, file_path):
        super().__init__(file_path)

    def parse(self):
        raise NotImplementedError

    def tokenize(self):
        print("Tokenizing pptx file")

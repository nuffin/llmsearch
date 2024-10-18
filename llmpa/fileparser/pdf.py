from .base import BaseFileParser


class PdfFileParser(BaseFileParser):
    def __init__(self, file_path):
        super().__init__(file_path)

    def parse(self):
        print("Parsing pdf file")

    def tokenize(self):
        print("Tokenizing pdf file")

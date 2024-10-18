from .base import BaseFileParser


class TextFileParser(BaseFileParser):
    def __init__(self, file_path):
        super().__init__(file_path)

    def parse(self):
        print("Parsing text file")

    def tokenize(self):
        print(
            f"Tokenizing file: {self.file_path} ({self.file_type}): {self.file_mimetype_name}"
        )

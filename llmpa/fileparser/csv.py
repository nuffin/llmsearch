from .base import BaseFileParser


class CsvFileParser(BaseFileParser):
    def __init__(self, file_path):
        super().__init__(file_path)

    def parse(self):
        print("Parsing csv file")

    def tokenize(self):
        print("Tokenizing csv file")

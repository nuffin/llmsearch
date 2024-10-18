from .base import BaseFileParser


class VideoFileParser(BaseFileParser):
    def __init__(self, file_path):
        super().__init__(file_path)

    def parse(self):
        print("Parsing video file")

    def tokenize(self):
        print("Tokenizing video file")

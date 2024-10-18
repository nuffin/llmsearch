class BaseFileParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_type = None

    def parse(self):
        raise NotImplementedError

    def tokenize(self):
        raise NotImplementedError

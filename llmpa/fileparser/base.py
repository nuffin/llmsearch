class BaseFileParser:
    def __init__(self, file_path):
        from .mimetype import detect, mimetypes_names

        self.file_path = file_path
        self.file_type = detect(file_path)
        self.file_mimetype_name = mimetypes_names[self.file_type]

    def parse(self):
        raise NotImplementedError

    def tokenize(self):
        raise NotImplementedError

    def prompt_for_tokenizing(self):
        return f"this is a {self.file_mimetype_name} file, tokenize it, and return the embeddings"

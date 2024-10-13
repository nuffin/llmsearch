class ClientBase:
    def embedding_text(self, text: str):
        raise NotImplementedError

    def embedding_image(self, filepath: str):
        raise NotImplementedError

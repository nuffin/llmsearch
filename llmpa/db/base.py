from typing import List

class BaseClient:
    def __init__(
        self,
        database_uri: f"http://localhost:19530",
        db_name="default",
    ):
        self.client = None
        self.database_uri = database_uri
        self.db_name = db_name

    def safe_embeddings(self, data_type, data_id, embeddings):
        raise NotImplementedError

    def search_embedding(self, data_type, query_embedding, limit=10, metric_type="L2"):
        raise NotImplementedError

    def get_embedding_by_id(self, data_type, data_id):
        raise NotImplementedError

    def get_embedding_by_ids(self, data_type, ids: List[str]):
        raise NotImplementedError

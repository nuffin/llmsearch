from typing import List
from pymilvus import MilvusClient, FieldSchema, DataType
from uuid import uuid4

from .base import BaseClient

_dims = {
        "text": 768,

        ## embedding lenth of image from different models
        "image": 512,
        "image_efficientnet": 1280,
        "image_resnet": 2048,

        "audio": 1024,
        "video": 1280,
        }


class Client(BaseClient):
    def __init__(
        self,
        database_uri: f"http://localhost:19530",
        db_name="default",
    ):
        super(Client, self).__init__(database_uri, db_name)
        self.client = MilvusClient(uri=database_uri, db_name=db_name)
        self.init_collections()

    def init_collections(self):
        collections = self.list_collections()
        for name in _dims.keys():
            collection_name = f"{name}_embeddings"
            if collection_name not in collections:
                self.create_collection(collection_name, _dims[name])

    def list_collections(self):
        collections = self.client.list_collections()
        return collections

    def create_collections(self):
        for name in _dims.keys():
            collection_name = f"{name}_embeddings"
            self.create_collection(collection_name, _dims[name])

    def drop_collections(self):
        collections = self.list_collections()
        for collection_name in collections:
            self.drop_collection(collection_name)

    def get_collection_name_by_data_type(self, data_type):
        return f"{data_type}_embeddings"

    def create_collection(self, collection_name, dim):
        name = collection_name.removesuffix("_embeddings")
        schema = self.client.create_schema(auto_id=False, primary_field="id")
        schema.add_field(
            field_name="id", datatype=DataType.INT64, auto_id=True, is_primary=True
        )
        schema.add_field(field_name="data_id", datatype=DataType.VARCHAR, max_length=64)
        schema.add_field(
            field_name=f"{name}_embedding", datatype=DataType.FLOAT_VECTOR, dim=dim
        )
        self.client.create_collection(collection_name, schema=schema)

        use_gpu = True  ## getenv("USE_GPU", False)
        embedding_index_type = "GPU_IVF_FLAT" if use_gpu else "IVF_FLAT"

        index_params = self.client.prepare_index_params()
        index_params.add_index(field_name="data_id", index_type="Trie")
        index_params.add_index(
            field_name=f"{name}_embedding",
            index_type=embedding_index_type,
            metric_type="L2",
            params={"nlist": 1024},
        )
        self.client.create_index(
            collection_name=collection_name, index_params=index_params
        )

    def drop_collection(self, collection_name):
        if self.client.has_collection(collection_name=collection_name):
            self.client.drop_collection(collection_name=collection_name)
            print(f"Collection '{collection_name}' dropped successfully.")
        else:
            print(f"Collection '{collection_name}' does not exist.")

    def save_embeddings(self, data_type, data_id, embeddings):
        if embeddings is None:
            return False
        collection_name = self.get_collection_name_by_data_type(data_type)
        self.client.insert(
            collection_name=f"{collection_name}",
            data=[
                {"data_id": data_id, f"{data_type}_embedding": embeddings.tolist()},
            ],
        )
        return True

    def search_embedding(self, data_type, query_embedding, limit=10, metric_type="L2"):
        query_embedding = (
            query_embedding.tolist()
            if isinstance(query_embedding, np.ndarray)
            else query_embedding
        )

        search_params = {
            "metric_type": metric_type,  # L2 or IP (Inner Product) or other supported metrics
            "params": {},  # nprobe is used for IVF index search, adjust as needed
        }

        # Perform the search
        collection_name = self.get_collection_name_by_data_type(data_type)
        print(f"Searching in collection '{collection_name}'...")
        self.client.load_collection(collection_name=collection_name, replica_number=1)
        results = self.client.search(
            collection_name=collection_name,
            data=[query_embedding],
            anns_field=f"{data_type}_embedding",
            search_param=search_params,
            limit=limit,
        )
        for result in results[0]:
            print(f"search: result={result}")

        return [
            {"id": result["id"], "distance": result["distance"]}
            for result in results[0]
        ]

    def get_embedding_by_id(self, data_type, data_id):
        ## collection_name = self.get_collection_name_by_data_type(data_type)
        ## self.client.load_collection(collection_name=collection_name, replica_number=1)
        ## results = self.client.get(collection_name=collection_name, ids=[data_id])
        ## return results
        return self.get_embedding_by_ids(data_type, [data_id])

    def get_embedding_by_ids(self, data_type, ids: List[str]):
        collection_name = self.get_collection_name_by_data_type(data_type)
        self.client.load_collection(collection_name=collection_name, replica_number=1)
        results = self.client.get(collection_name=collection_name, ids=ids)
        return results[0]


# Example Usage
if __name__ == "__main__":
    # Initialize Milvus client
    milvus_client = Client("http://localhost:59530")
    collections = milvus_client.list_collections()
    print(f"Existing collections: {collections}")

    milvus_client.drop_collections()
    milvus_client.create_collections()

    # Example embeddings (replace these with actual embeddings from your model)
    import numpy as np

    video_embeddings = np.random.rand(
        1280
    )  # Example 1280-dimensional embeddings for video
    image_embeddings = np.random.rand(
        512
    )  # Example 512-dimensional embeddings for image
    audio_embeddings = np.random.rand(
        1024
    )  # Example 1024-dimensional embeddings for audio
    text_embeddings = np.random.rand(768)  # Example 768-dimensional embeddings for text

    # Process and save embeddings
    video_id = str(uuid4())
    milvus_client.save_embeddings("video", video_id, video_embeddings)
    image_id = str(uuid4())
    milvus_client.save_embeddings("image", image_id, image_embeddings)
    audio_id = str(uuid4())
    milvus_client.save_embeddings("audio", audio_id, audio_embeddings)
    text_id = str(uuid4())
    milvus_client.save_embeddings("text", text_id, text_embeddings)

    results = milvus_client.search_embedding(
        "video", video_embeddings, limit=5, metric_type="L2"
    )
    print("results:", results)

    # data = milvus_client.get_embedding_by_ids("video", [x["id"] for x in results])
    # print(data)

    for result in results:
        data = milvus_client.get_embedding_by_id("video", result["id"])
        print(data)

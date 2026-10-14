from dataclasses import asdict

from qdrant_client import AsyncQdrantClient, models
from qdrant_client.http.models import PointStruct

from app.conf.app_config import app_config
from app.entities.metric_info import MetricInfo


class MetricQdrantRepository:
    def __init__(self, client:AsyncQdrantClient):
        self.client = client
    collection_name  = "data-agent-metric"

    async def recreate_collection(self):
        if await self.client.collection_exists(collection_name=self.collection_name):
            await self.client.delete_collection(collection_name=self.collection_name)
        await self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size = app_config.qdrant.embedding_size,
                distance=models.Distance.COSINE
            )
        )

    async def upsert(self, ids:list[str], embeddings:list[list[float]], payloads:list[MetricInfo], batch_size:int = 10):
        zipped = list(zip(ids, embeddings, payloads))

        for i in range(0, len(zipped), batch_size):
            batch = zipped[i:i+batch_size]
            points = [
                PointStruct(
                    id = id,
                    vector=embedding,
                    payload=asdict(payload)
                ) for id, embedding, payload in batch
            ]
            await self.client.upsert(collection_name=self.collection_name,points=points)

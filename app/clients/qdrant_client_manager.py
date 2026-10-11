import asyncio
import uuid
from typing import Optional
from qdrant_client import AsyncQdrantClient, models
from sqlalchemy.util import await_

from app.clients.embedding_client_manager import embedding_client_manager
from app.conf.app_config import QdrantConfig, app_config


class QdrantClientManager:
    def __init__(self, qdrant_config:QdrantConfig):
        self.qdrant_config = qdrant_config
        self.client:Optional[AsyncQdrantClient] = None

    def _get_url(self):
        return f"http://{self.qdrant_config.host}:{self.qdrant_config.port}"

    def init(self):
        self.client = AsyncQdrantClient(self._get_url())

    async def close(self):
        if self.client is not None:
            await self.client.close()


qdrant_client_manager = QdrantClientManager(app_config.qdrant)


async def test_collection():    #建立集合
    result = await client.collection_exists(collection_name="test1")
    print(result)

    if not result:
        result = await client.create_collection(
            collection_name=coll_name,
            vectors_config=models.VectorsConfig(
                size=qdrant_client_manager.qdrant_config.embedding_size,
                distance=models.Distance.COSINE
            )
        )
        print(result)


async def test_add_points():    #插入向量点数据
    keywords = ["苹果", "香蕉", "葡萄", "开发工程师", "Java开发工程师", "Python开发工程师", "C++开发工程师",
                "C#开发工程师", "PHP开发工程师", "Ruby开发工程师", "Go开发工程师", "JavaScript开发工程师",
                "Swift开发工程师", "Kotlin开发工程师", "Rust开发工程师", "Perl开发工程师", "Lua开发工程师",
                "VB.NET开发工程师", "Objective-C开发工程师", "Scal"]

    points = [models.PointStruct(
        id=str(uuid.uuid4()),
        vector=await embedding_client_manager.client.aembed_query(keyword),
        payload={"keyword": keyword}  # 上传元数据
    ) for keyword in keywords]
    await client.upsert(
        collection_name=coll_name,
        points=points
    )


# asyncio.run(test_add_points())

async def test_search():    #查询向量点数据
    query_keyword = "开发工程师"
    result = await client.query_points(
        collection_name=coll_name,
        query=await embedding_client_manager.client.aembed_query(query_keyword),
        limit=5,
        score_threshold=0.7
    )
    result_points = [point.payload for point in result.points]
    print(result_points)

if __name__ == '__main__':
    qdrant_client_manager.init()
    embedding_client_manager.init()
    client = qdrant_client_manager.client
    coll_name = "test1"

    asyncio.run(test_search())


import asyncio
from typing import Optional
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings

from app.conf.app_config import EmbeddingConfig, app_config


class EmbeddingClientManager:

    def __init__(self,embedding_config:EmbeddingConfig):
        self.embedding_config = embedding_config
        self.client:Optional[HuggingFaceEndpointEmbeddings] = None

    def _get_url(self):
        return f"http://{self.embedding_config.host}:{self.embedding_config.port}"


    def init(self):
        self.client = HuggingFaceEndpointEmbeddings(model=self._get_url())

embedding_client_manager = EmbeddingClientManager(app_config.embedding)

if __name__ == "__main__":
    embedding_client_manager.init()
    client = embedding_client_manager.client

    async def test_embedding():
        # result = await client.aembed_query("你好")      #单个进行向量化

        # list = ["你好","hello"]
        # result = await client.aembed_documents(list)  #整个列表一同进行向量化

        list1 = [f"数字{i}" for i in range(25)]

        #采用分批次方式, 每次对10个字符串进行embedding
        batch_size = 10
        for i in range(0, len(list1), batch_size):
            texts = list1[i:i+batch_size]
            result = await client.aembed_documents(texts)
        print(result)

    asyncio.run(test_embedding())

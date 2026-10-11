import asyncio
import random

from elasticsearch import AsyncElasticsearch
from sqlalchemy.util import await_

from app.conf.app_config import ESConfig, app_config


class ESClientManager:
    def __init__(self, es_config:ESConfig):
        self.es_config = es_config
        self.client = None


    def _get_url(self):
        return f"http://{self.es_config.host}:{self.es_config.port}"

    def init(self):
        self.client = AsyncElasticsearch(hosts=self._get_url())

    async def close(self):
        if self.client is not None:
            await self.client.close()

es_client_manager = ESClientManager(app_config.es)

if __name__ == "__main__":
    es_client_manager.init()
    client = es_client_manager.client

    index_name = "product"

    async def test_index():     #建立索引
        result = await client.indices.exists(index = index_name)
        print(result)
        if not result:
            result = await client.indices.create(
                index = index_name,
                mappings={
                    "properties": {
                        "name":{
                            "type":"text",
                            "analyzer": "ik_max_word"
                        },
                        "brand":{
                            "type":"keyword",
                        },
                        "price":{
                            "type":"float",
                        }
                    }
                }
            )
            print(result)
        await es_client_manager.close()

    async def test_add_doc():   #新增单个数据
        result = await client.index(
            index = index_name,
            document = {
                "name":"华为手机meta80",
                "brand":"华为",
                "price":9888
            }
        )
        await es_client_manager.close()
        print(result)


    async def test_add_docs():  #新增多条数据
        operations = []
        goods_list = ["小米手机116","小米汽车","华为手机meta90","华为汽车","苹果手机","苹果汽车"]
        for goods in goods_list:
            operations.append({
                "index":{"_index":index_name}
            })
            operations.append({
                "name":goods,
                "price":random.randint(1000,9999),
                "brand":"小米"
            })
        result = await client.bulk(operations=operations)   #operations里面要一条指定一条文档,所以每次都是都要给索引进行解析
        await es_client_manager.close()
        print(result)

    asyncio.run(test_add_docs())


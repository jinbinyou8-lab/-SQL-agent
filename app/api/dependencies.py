from fastapi import Depends
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from openai import embeddings
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.clients import mysql_client_manager
from app.clients.embedding_client_manager import embedding_client_manager
from app.clients.es_client_manager import es_client_manager
from app.clients.mysql_client_manager import meta_mysql_client_manager, dw_mysql_client_manager
from app.clients.qdrant_client_manager import qdrant_client_manager
from app.repositories.es.value_es_repository import ValueESRepository
from app.repositories.mysql.dw import dw_mysql_repository
from app.repositories.mysql.dw.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta import meta_mysql_repository
from app.repositories.mysql.meta.meta_mysql_repository import MetaMySQLRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository
from app.services.query_service import QueryService



# async def get_column_qdrant_repository():
#     return ColumnQdrantRepository(qdrant_client_manager.client)
#
# async def get_embedding_client():
#     return embedding_client_manager.client
#
# async def get_metric_qdrant_repository():
#     return MetricQdrantRepository(qdrant_client_manager.client)
#
# async def get_value_es_repository():
#     return ValueESRepository(es_client_manager.client)
#
# async def get_meta_session():
#     async with meta_mysql_client_manager.session_factory() as meta_session:
#         yield meta_session  #查询前会获取到session, 执行DB操作, 完成DB操作后, 自动关闭Session
#
# async def get_meta_mysql_repository(session:AsyncSession = Depends(get_meta_session)):
#     return MetaMySQLRepository(session)
#
# async def get_dw_session():
#     async with dw_mysql_client_manager.session_factory() as dw_session:
#         yield dw_session
#
# async def get_dw_mysql_repository(session:AsyncSession = Depends(get_dw_session)):
#     return DWMySQLRepository(session)
#
#
# async def get_query_service(
#         embedding_client:HuggingFaceEndpointEmbeddings = Depends(get_embedding_client),
#         column_qdrant_repository:ColumnQdrantRepository = Depends(get_column_qdrant_repository),
#         metric_qdrant_repository:MetricQdrantRepository = Depends(get_metric_qdrant_repository),
#         value_es_repository:ValueESRepository = Depends(get_value_es_repository),
#         meta_mysql_repository:MetaMySQLRepository = Depends(get_meta_mysql_repository),
#         dw_mysql_repository:DWMySQLRepository = Depends(get_dw_mysql_repository)
#     ):
#     return QueryService(
#         embedding_client=embedding_client,
#         column_qdrant_repository=column_qdrant_repository,
#         metric_qdrant_repository=metric_qdrant_repository,
#         value_es_repository=value_es_repository,
#         meta_mysql_repository=meta_mysql_repository,
#         dw_mysql_repository=dw_mysql_repository,
#     )

_embedding_client = None
_value_es_repository = None
_column_qdrant_repository = None
_metric_qdrant_repository = None
_meta_mysql_repository = None
_dw_mysql_repository = None

def init_global_instance():
    global _embedding_client
    global _value_es_repository
    global _column_qdrant_repository
    global _metric_qdrant_repository
    global _meta_mysql_repository
    global _dw_mysql_repository
    _embedding_client = embedding_client_manager.client
    _value_es_repository = ValueESRepository(es_client_manager.client)
    _column_qdrant_repository = ColumnQdrantRepository(qdrant_client_manager.client)
    _metric_qdrant_repository = MetricQdrantRepository(qdrant_client_manager.client)
    _meta_mysql_repository = MetaMySQLRepository(None)
    _dw_mysql_repository = DWMySQLRepository(None)




async def get_column_qdrant_repository():
    return _column_qdrant_repository

async def get_embedding_client():
    return _embedding_client

async def get_metric_qdrant_repository():
    return _metric_qdrant_repository

async def get_value_es_repository():
    return _value_es_repository

async def get_meta_session():
    async with meta_mysql_client_manager.session_factory() as meta_session:
        yield meta_session  #查询前会获取到session, 执行DB操作, 完成DB操作后, 自动关闭Session

async def get_meta_mysql_repository(session:AsyncSession = Depends(get_meta_session)):
    _meta_mysql_repository.session = session
    return _meta_mysql_repository

async def get_dw_session():
    async with dw_mysql_client_manager.session_factory() as dw_session:
        yield dw_session

async def get_dw_mysql_repository(session:AsyncSession = Depends(get_dw_session)):
    _dw_mysql_repository.session = session
    return _dw_mysql_repository


async def get_query_service(
        embedding_client:HuggingFaceEndpointEmbeddings = Depends(get_embedding_client),
        column_qdrant_repository:ColumnQdrantRepository = Depends(get_column_qdrant_repository),
        metric_qdrant_repository:MetricQdrantRepository = Depends(get_metric_qdrant_repository),
        value_es_repository:ValueESRepository = Depends(get_value_es_repository),
        meta_mysql_repository:MetaMySQLRepository = Depends(get_meta_mysql_repository),
        dw_mysql_repository:DWMySQLRepository = Depends(get_dw_mysql_repository)
    ):
    return QueryService(
        embedding_client=embedding_client,
        column_qdrant_repository=column_qdrant_repository,
        metric_qdrant_repository=metric_qdrant_repository,
        value_es_repository=value_es_repository,
        meta_mysql_repository=meta_mysql_repository,
        dw_mysql_repository=dw_mysql_repository,
    )
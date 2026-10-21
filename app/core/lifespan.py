from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.dependencies import init_global_instance
from app.clients.embedding_client_manager import embedding_client_manager
from app.clients.es_client_manager import es_client_manager
from app.clients.mysql_client_manager import dw_mysql_client_manager, meta_mysql_client_manager
from app.clients.qdrant_client_manager import qdrant_client_manager


@asynccontextmanager
async def lifespan(app:FastAPI):
    """
    app.lifespan()方法, 用于在应用程序启动和停止时执行一些操作
    :param app:
    :return:
    """
    # 在应用程序启动时执行一些操作
    print("启动应用前执行初始操作")
    embedding_client_manager.init()
    qdrant_client_manager.init()
    es_client_manager.init()
    meta_mysql_client_manager.init()
    dw_mysql_client_manager.init()

    init_global_instance()
    yield
    #在应用程序停止时执行一些操作
    print("应用停止时执行清理操作")
    await qdrant_client_manager.close()
    await es_client_manager.close()
    await dw_mysql_client_manager.close()
    await meta_mysql_client_manager.close()
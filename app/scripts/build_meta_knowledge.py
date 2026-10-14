from argparse import ArgumentParser
from pathlib import Path
import asyncio
from sys import argv

from app.clients.embedding_client_manager import embedding_client_manager
from app.clients.es_client_manager import es_client_manager
from app.clients.mysql_client_manager import dw_mysql_client_manager, meta_mysql_client_manager
from app.clients.qdrant_client_manager import qdrant_client_manager
from app.core.log import logger
from app.repositories.es.value_es_repository import ValueESRepository
from app.repositories.mysql.dw.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta.meta_mysql_repository import MetaMySQLRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository
from app.services.meta_knowledge_service import MetaKnowledgeService

# 默认元数据配置文件: 项目根目录下的 conf/meta_config.yaml
# 不传 -c 参数时使用, 避免 Path(None) 报 TypeError
DEFAULT_META_CONFIG = Path(__file__).resolve().parents[2] / "conf" / "meta_config.yaml"


async def build(meta_config_path: Path):
    #测试脚本执行获取到配置文件
    logger.info(meta_config_path)

    #1. 初始化操作
    dw_mysql_client_manager.init()
    meta_mysql_client_manager.init()
    qdrant_client_manager.init()
    embedding_client_manager.init()
    es_client_manager.init()
    #2. 创建业务层对象, 调用元数据库业务层对象完成源数据库构建
    async with (dw_mysql_client_manager.session_factory() as dw_session, meta_mysql_client_manager.session_factory() as meta_session):
        meta_knowledge_service = MetaKnowledgeService(
            dw_mysql_repository=DWMySQLRepository(dw_session),
            meta_mysql_repository=MetaMySQLRepository(meta_session),
            column_qdrant_repository=ColumnQdrantRepository(qdrant_client_manager.client),
            embedding_client=embedding_client_manager.client,
            value_es_repository=ValueESRepository(es_client_manager.client),
            metric_qdrant_repository=MetricQdrantRepository(qdrant_client_manager.client),
        )
        await meta_knowledge_service.build(meta_config_path)
        await dw_mysql_client_manager.close()
        await meta_mysql_client_manager.close()
        await qdrant_client_manager.close()
        await es_client_manager.close()
        await qdrant_client_manager.close()

if __name__ == "__main__":
   # logger.info(argv)
   #1. 获取到命令行参数 目的: 获取增量动态新增配置信息 sys.argv通过索引获取命令行参数  不方便维护
   #1,1 构建参数解析器对象ArgumentParser
   parser = ArgumentParser()
   #1.2 添加可选命令参数名称或标记名称 对应命令行参数中: xx.py -c
   parser.add_argument('-c', '--conf', type=Path, default=DEFAULT_META_CONFIG,
                       help='元数据配置文件路径, 默认 conf/meta_config.yaml')
   #1.3 解析并将提取的数据
   args = parser.parse_args()
   #2. 调用脚本
   asyncio.run(build(args.conf))
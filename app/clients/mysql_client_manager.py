import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.conf.app_config import DBConfig, app_config


class MySQLClientManager:

    def __init__(self, db_config: DBConfig):
        #通过构造传入数据库的配置信息
        self.db_config = db_config
        #设计engine实例属性
        self.engine = None
        self.session_factory = None

    def _get_url(self):
        return f"mysql+asyncmy://{self.db_config.user}:{self.db_config.password}@{self.db_config.host}:{self.db_config.port}/{self.db_config.database}?charset=utf8mb4"


    def init(self):
        self.engine = create_async_engine(self._get_url(), echo=False)
        self.session_factory = async_sessionmaker(self.engine)

    async def close(self):
        if self.engine is not None:
            await self.engine.dispose()



dw_mysql_client_manager = MySQLClientManager(app_config.db_dw)
meta_mysql_client_manager = MySQLClientManager(app_config.db_meta)


if __name__ == "__main__":
    dw_mysql_client_manager.init()

    # async def test_by_engine():
    #     async with AsyncSession(dw_mysql_client_manager.engine) as dw_session:
    #         result = await dw_session.execute(text("show tables;")) #只进行发命令,但是不会把结果交给我们,因此需要scalars().fetchall()
    #         print(result.scalars().fetchall())
    #         await dw_mysql_client_manager.close()
    # asyncio.run(test_by_engine())



    async def test_by_session_maker():#使用session工厂
        async with dw_mysql_client_manager.session_factory() as dw_session:
            result = await dw_session.execute(text("show tables;"))  # 只进行发命令,但是不会把结果交给我们,因此需要scalars().fetchall()
            print(result.scalars().fetchall())
            await dw_mysql_client_manager.close()
    asyncio.run(test_by_session_maker())
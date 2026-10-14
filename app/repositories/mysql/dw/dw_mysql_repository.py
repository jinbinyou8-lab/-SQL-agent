from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import text


class DWMySQLRepository:
    """
    用户操作dw数据库持久层
    """

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_column_types(self, table_name) -> dict[str, str]:
        """
        根据表名获取该表下所有字段的类型
        :param name:
        :return:
        """
        sql = f"show COLUMNS from {table_name}"
        result = await self.session.execute(text(sql))
        #自定义SQL 结果获取通过result.fetchall()函数获取
        return {row.Field: row.Type for row in result.fetchall()}

    async def get_column_values(self, table_name, column_name, limit=10):
        sql = f"select distinct {column_name} from {table_name} limit {limit}"
        result = await self.session.execute(text(sql))
        return result.scalars().fetchall()
import aiohttp
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger


async def validate_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer({"type": "progress", "step": "校验sql", "status": "running"})
    try:
        # 1. 获取状态中SQL
        sql = state["sql"]
        # 2. 验证SQL
        dw_mysql_repository = runtime.context["dw_mysql_repository"]
        await dw_mysql_repository.validate_sql(sql)
        writer({"type": "progress", "step": "校验sql", "status": "success"})
        return {"error": None}
    except Exception as e:
        writer({"type": "progress", "step": "校验sql", "status": "error"})
        logger.error(f"校正sql语句失败, 错误信息:{str(e)}")
        return {"error": str(e)}
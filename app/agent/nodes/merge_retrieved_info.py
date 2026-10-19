
from langgraph.runtime import Runtime
from app.core.log import logger
from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState, MetricInfoState


async def merge_retrieved_info(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer({"type":"progress", "step":"合并信息", "status":"running"})


    #1. 合并所有字段, 将已召回指标,字段取值 列表中包含字段信息 合并到已召回字段 (记得去重,字段取值加入到字段examples中)
    retrieved_metrics = state["retrieved_metrics"]

    #2. 按table_id分组 得到表跟字段列表映射字典 {"table_id1":[{ColumnInfo1}, {ColumnInfo1}], "table_id2":[{ColumnInfo2}, {ColumnInfo2}]}


    #3. 对相关表显示增加主外键字段信息


    #4. 封装state中表信息列表: list[TableInfoState]


    #5. 封装state中指标信息列表: list[MetricInfoState]
    metric_infos:list[MetricInfoState] = [MetricInfoState(
        name= retrieved_metric.name,
        description= retrieved_metric.description,
        relevant_columns=retrieved_metric.relevant_columns,
        alias=retrieved_metric.alias,
    ) for retrieved_metric in retrieved_metrics]
    logger.info(f"合并信息, 指标列表: {[metric_info["name"] for metric_info in metric_infos]}")

    #6. 更新state中表信息列表,指标信息列表
    return {"metric_infos":metric_infos}
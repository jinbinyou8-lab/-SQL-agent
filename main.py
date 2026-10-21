import time
import uuid

from fastapi import FastAPI, Query, Path, Request

from app.api.routers.hello_router import hello_router
from app.api.routers.query_router import query_router
from app.core.context import request_id_ctx_var
from app.core.lifespan import lifespan

#1. 创建FastAPI实例
app = FastAPI(lifespan=lifespan)

#2. 导入路由
app.include_router(hello_router)
app.include_router(query_router)

#3. 为实例设置中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    #调用路由函数前, 为上下文变量赋值
    request_id_ctx_var.set(uuid.uuid4())
    # 调用路由函数
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

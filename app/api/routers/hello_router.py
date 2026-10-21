from fastapi import APIRouter, Query, Path

#创建路由对象
hello_router = APIRouter()

#2. 创建用于测试Http接口
@hello_router.get("/hello/{address}")
async def hello(name:str=Query(min_length=2, max_length=6), address:str=Path(min_length=3, max_length=6)):
    return {"message":f"Hello {name}, 来自{address}"}
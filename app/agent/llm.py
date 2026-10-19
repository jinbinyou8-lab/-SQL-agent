import asyncio
import os

from langchain_openai import ChatOpenAI

from app.conf.app_config import app_config

# api_key 从配置文件读取(conf/app_config.yaml 已被 .gitignore 忽略); 配置里没填时回退到环境变量
llm = ChatOpenAI(
    model = "deepseek-flash",
    temperature=0,
    api_key=app_config.llm.api_key or os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

if __name__=="__main__":
    async def test():
        result = await llm.ainvoke("你是谁")
        print(result.content)
    asyncio.run(test())
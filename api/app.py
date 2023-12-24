from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
async def read_root():
    """
    异步函数，返回一个包含键值对的字典对象。
    字典中的键为"Hello"，值为"World"。
    """
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    """
    异步函数，用于读取项目条目。

    参数:
        item_id (int): 条目ID
        q (str, optional): 可选参数，查询问题

    返回:
        dict: 包含条目ID和查询问题的字典
    """
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
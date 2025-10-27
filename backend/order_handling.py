from pydantic import BaseModel
from typing import Any

class BaseOrder(BaseModel):
    payload: Any
    predicates: list[Any]



from fastapi import APIRouter

router = APIRouter()

@router.post("/order")
async def handle_order(body: BaseOrder) -> bool:
    return True
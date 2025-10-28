from pydantic import BaseModel
from typing import Any
from entities.order import OrderParameter

class PlaceOrder(BaseModel):
    payload: Any
    parameters: list[OrderParameter]

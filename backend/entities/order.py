from typing import TypedDict, Any
from uuid import UUID

from entities.common import ParameterType

class OrderParameter(TypedDict):
    name: str
    type: ParameterType
    value: Any # depends on OrderParameterType(to serializing)

class Order(TypedDict):
    id: UUID
    payload: Any # serializable data
    parameters: list[OrderParameter]

from pydantic import BaseModel
from typing import Optional
from entities.worker import WorkerParameterDescription

class CreateWorker(BaseModel):
    parameters_declaration: list[WorkerParameterDescription]
    parameters_expression: str

class UpdateWorker(BaseModel):
    parameters_declaration: Optional[list[WorkerParameterDescription]] = None
    parameters_expression: Optional[str] = None
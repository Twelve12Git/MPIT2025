from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from typing import List

from db.base import BaseModel
from db.types import PrimaryKey

from entities.common import ParameterType


class WorkerParameterDescriptionModel(BaseModel):
    __tablename__ = "worker_parameter_descriptions"
    
    id: Mapped[PrimaryKey]
    worker_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("worker.id", ondelete="CASCADE"), 
        index=True
    )
    type: Mapped[ParameterType]
    name: Mapped[str] = mapped_column(index=True)
    
    # Relationship back to worker
    worker: Mapped["WorkerModel"] = relationship(
        back_populates="parameters_declaration"
    )


class WorkerModel(BaseModel):    
    id: Mapped[PrimaryKey]
    parameters_expression: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Relationship to parameter descriptions
    parameters_declaration: Mapped[List["WorkerParameterDescriptionModel"]] = relationship(
        back_populates="worker",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
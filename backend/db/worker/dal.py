from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from typing import List, Optional

from db.base import BaseDAL
from db.exceptions import EntityAlreadyExist, EntityNotFound
from .model import WorkerModel, WorkerParameterDescriptionModel
from entities.common import ParameterType


class WorkerParameterDescriptionDAL(BaseDAL):
    async def create(
        self, 
        worker_id: UUID, 
        type: ParameterType, 
        name: str
    ) -> WorkerParameterDescriptionModel:
        try:
            parameter_description = WorkerParameterDescriptionModel(
                worker_id=worker_id,
                type=type,
                name=name
            )
            self.session.add(parameter_description)
            await self.session.flush()
            await self.session.refresh(parameter_description)
            return parameter_description
        except IntegrityError as e:
            await self.session.rollback()
            raise EntityAlreadyExist(f"Parameter description with name '{name}' already exists for this worker") from e

    async def get_by_worker_id(self, worker_id: UUID) -> List[WorkerParameterDescriptionModel]:
        query = select(WorkerParameterDescriptionModel).where(
            WorkerParameterDescriptionModel.worker_id == worker_id
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, id: UUID) -> WorkerParameterDescriptionModel:
        query = select(WorkerParameterDescriptionModel).where(
            WorkerParameterDescriptionModel.id == id
        )
        result = await self.session.execute(query)
        parameter_description = result.scalar_one_or_none()
        
        if not parameter_description:
            raise EntityNotFound(f"Parameter description with id {id} not found")
        return parameter_description

    async def delete(self, id: UUID) -> WorkerParameterDescriptionModel:
        parameter_description = await self.get_by_id(id)
        await self.session.delete(parameter_description)
        await self.session.flush()
        return parameter_description

    async def delete_by_worker_id(self, worker_id: UUID) -> None:
        query = delete(WorkerParameterDescriptionModel).where(
            WorkerParameterDescriptionModel.worker_id == worker_id
        )
        await self.session.execute(query)


class WorkerDAL(BaseDAL):
    async def create(
        self, 
        parameters_expression: Optional[str] = None,
        parameters_declaration: Optional[List[dict]] = None
    ) -> WorkerModel:
        try:
            worker = WorkerModel(
                parameters_expression=parameters_expression
            )
            self.session.add(worker)
            await self.session.flush()
            
            # Создаем параметры описания, если они предоставлены
            if parameters_declaration:
                parameter_dal = WorkerParameterDescriptionDAL(self.session)
                for param_data in parameters_declaration:
                    await parameter_dal.create(
                        worker_id=worker.id,
                        type=param_data['type'],
                        name=param_data['name']
                    )
            
            await self.session.refresh(worker)
            return worker
        except IntegrityError as e:
            await self.session.rollback()
            raise EntityAlreadyExist(f"Worker creation failed: {e}") from e

    async def get(self, id: UUID) -> WorkerModel:
        query = select(WorkerModel).where(WorkerModel.id == id)
        result = await self.session.execute(query)
        worker = result.scalar_one_or_none()
        
        if not worker:
            raise EntityNotFound(f"Worker with id {id} not found")
        return worker

    async def get_with_parameters(self, id: UUID) -> WorkerModel:
        query = select(WorkerModel).where(WorkerModel.id == id)
        result = await self.session.execute(query)
        worker = result.scalar_one_or_none()
        
        if not worker:
            raise EntityNotFound(f"Worker with id {id} not found")
        
        # Явно загружаем параметры, если они еще не загружены
        if not worker.parameters_declaration:
            parameter_dal = WorkerParameterDescriptionDAL(self.session)
            worker.parameters_declaration = await parameter_dal.get_by_worker_id(id)
        
        return worker

    async def update(
        self, 
        id: UUID, 
        parameters_expression: Optional[str] = None,
        parameters_declaration: Optional[List[dict]] = None
    ) -> WorkerModel:
        worker = await self.get(id)
        
        if parameters_expression is not None:
            worker.parameters_expression = parameters_expression
        
        # Обновляем параметры описания, если они предоставлены
        if parameters_declaration is not None:
            parameter_dal = WorkerParameterDescriptionDAL(self.session)
            # Удаляем старые параметры
            await parameter_dal.delete_by_worker_id(id)
            # Создаем новые
            for param_data in parameters_declaration:
                await parameter_dal.create(
                    worker_id=id,
                    type=param_data['type'],
                    name=param_data['name']
                )
        
        await self.session.flush()
        await self.session.refresh(worker)
        return worker

    async def delete(self, id: UUID) -> WorkerModel:
        worker = await self.get(id)
        await self.session.delete(worker)
        await self.session.flush()
        return worker

    async def list_all(self) -> List[WorkerModel]:
        query = select(WorkerModel)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def exists(self, id: UUID) -> bool:
        query = select(WorkerModel.id).where(WorkerModel.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
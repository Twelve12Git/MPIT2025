from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from db.session import get_async_session
from db.worker.dal import WorkerDAL
from .schemas import CreateWorker, UpdateWorker
from entities.worker import Worker

worker_router = APIRouter(prefix="/workers", tags=["workers"])


@worker_router.post("/", response_model=Worker, status_code=status.HTTP_201_CREATED)
async def create_worker(
    body: CreateWorker, 
    session: AsyncSession = Depends(get_async_session)
) -> Worker:
    try:
        worker_dal = WorkerDAL(session)
        
        # Конвертируем Pydantic модели в словари для DAL
        parameters_declaration = [
            {
                "type": param.type,
                "name": param.name
            }
            for param in body.parameters_declaration
        ]
        
        worker = await worker_dal.create(
            parameters_expression=body.parameters_expression,
            parameters_declaration=parameters_declaration
        )
        
        # Конвертируем SQLAlchemy модель в Pydantic модель
        return Worker(
            id=worker.id,
            parameters_declaration=[
                WorkerParameterDescription(
                    type=param.type,
                    name=param.name
                )
                for param in worker.parameters_declaration
            ],
            parameters_expression=worker.parameters_expression
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create worker: {str(e)}"
        )


@worker_router.get("/{worker_id}", response_model=Worker)
async def get_worker(
    worker_id: UUID,
    session: AsyncSession = Depends(get_async_session)
) -> Worker:
    try:
        worker_dal = WorkerDAL(session)
        worker = await worker_dal.get_with_parameters(worker_id)
        
        return Worker(
            id=worker.id,
            parameters_declaration=[
                WorkerParameterDescription(
                    type=param.type,
                    name=param.name
                )
                for param in worker.parameters_declaration
            ],
            parameters_expression=worker.parameters_expression
        )
    except EntityNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get worker: {str(e)}"
        )


@worker_router.put("/{worker_id}", response_model=Worker)
async def update_worker(
    worker_id: UUID,
    body: UpdateWorker,
    session: AsyncSession = Depends(get_async_session)
) -> Worker:
    try:
        worker_dal = WorkerDAL(session)
        
        update_data = {}
        if body.parameters_expression is not None:
            update_data["parameters_expression"] = body.parameters_expression
        
        if body.parameters_declaration is not None:
            update_data["parameters_declaration"] = [
                {
                    "type": param.type,
                    "name": param.name
                }
                for param in body.parameters_declaration
            ]
        
        worker = await worker_dal.update(worker_id, **update_data)
        
        return Worker(
            id=worker.id,
            parameters_declaration=[
                WorkerParameterDescription(
                    type=param.type,
                    name=param.name
                )
                for param in worker.parameters_declaration
            ],
            parameters_expression=worker.parameters_expression
        )
    except EntityNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update worker: {str(e)}"
        )


@worker_router.delete("/{worker_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_worker(
    worker_id: UUID,
    session: AsyncSession = Depends(get_async_session)
) -> None:
    try:
        worker_dal = WorkerDAL(session)
        await worker_dal.delete(worker_id)
    except EntityNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete worker: {str(e)}"
        )


@worker_router.get("/", response_model=list[Worker])
async def list_workers(
    session: AsyncSession = Depends(get_async_session)
) -> list[Worker]:
    try:
        worker_dal = WorkerDAL(session)
        workers = await worker_dal.list_all()
        
        result = []
        for worker in workers:
            # Для каждого worker загружаем параметры отдельно
            worker_with_params = await worker_dal.get_with_parameters(worker.id)
            result.append(
                Worker(
                    id=worker_with_params.id,
                    parameters_declaration=[
                        WorkerParameterDescription(
                            type=param.type,
                            name=param.name
                        )
                        for param in worker_with_params.parameters_declaration
                    ],
                    parameters_expression=worker_with_params.parameters_expression
                )
            )
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list workers: {str(e)}"
        )
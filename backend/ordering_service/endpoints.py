import json
from uuid import UUID, uuid4
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio import Redis
from pydantic import BaseModel
from typing import Any

from entities.order import Order, OrderParameter
from entities.common import ParameterType
from settings import SETTINGS

# Роутер для заказов
order_router = APIRouter(prefix="/orders", tags=["orders"])

# Redis connection dependency
async def get_redis() -> Redis:
    redis = Redis(
        host=SETTINGS.REDIS.HOST,
        port=SETTINGS.REDIS.PORT,
        db=int(SETTINGS.REDIS.DB),
        password=SETTINGS.REDIS.PASSWORD.get_secret_value(),
        decode_responses=True,
        encoding="utf-8"
    )
    try:
        # Проверяем подключение
        await redis.ping()
        yield redis
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Redis connection failed: {str(e)}"
        )
    finally:
        await redis.close()

class CreateOrderRequest(BaseModel):
    payload: dict
    parameters: list[OrderParameter]

@order_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: CreateOrderRequest,
    redis: Redis = Depends(get_redis)
) -> dict:
    try:
        # Создаем Order объект
        order_id = uuid4()
        order: Order = {
            "id": order_id,
            "payload": order_data.payload,
            "parameters": order_data.parameters
        }
        
        # Валидация параметров
        await _validate_order_parameters(order)
        
        # Сериализуем заказ в JSON
        order_json = await _serialize_order(order)
        
        # Кладем в Redis очередь
        queue_name = "orders_queue"
        result = await redis.lpush(queue_name, order_json)
        
        # Сохраняем в хеш для отслеживания статуса
        order_hash_key = f"order:{order_id}"
        await redis.hset(order_hash_key, mapping={
            "payload": json.dumps(order['payload']),
            "status": "queued",
            "created_at": datetime.utcnow().isoformat(),
            "queue_position": result  # Позиция в очереди
        })
        
        # Устанавливаем TTL для хеша (24 часа)
        await redis.expire(order_hash_key, 24 * 60 * 60)
        
        return {
            "order_id": order_id,
            "status": "queued",
            "queue_position": result,
            "message": "Order successfully added to queue"
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create order: {str(e)}"
        )

async def _validate_order_parameters(order: Order) -> None:
    """Валидация параметров заказа"""
    for param in order['parameters']:
        # Проверяем тип параметра
        if not isinstance(param['name'], str):
            raise ValueError(f"Parameter name must be string, got {type(param['name'])}")
        
        # Проверяем соответствие типа и значения
        await _validate_parameter_value(param['type'], param['value'])

async def _validate_parameter_value(param_type: ParameterType, value: Any) -> None:
    """Валидация значения параметра в зависимости от типа"""
    try:
        if param_type == ParameterType.STRING:
            if not isinstance(value, str):
                raise ValueError(f"Expected string value for STRING type, got {type(value)}")
        
        elif param_type == ParameterType.INTEGER:
            if not isinstance(value, int):
                raise ValueError(f"Expected integer value for INTEGER type, got {type(value)}")
        
        elif param_type == ParameterType.FLOAT:
            if not isinstance(value, (int, float)):
                raise ValueError(f"Expected float value for FLOAT type, got {type(value)}")
        
        elif param_type == ParameterType.BOOLEAN:
            if not isinstance(value, bool):
                raise ValueError(f"Expected boolean value for BOOLEAN type, got {type(value)}")
        
        elif param_type == ParameterType.JSON:
            # Для JSON проверяем, что значение сериализуемо
            json.dumps(value)
        
        else:
            raise ValueError(f"Unsupported parameter type: {param_type}")
            
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid parameter value: {str(e)}")

async def _serialize_order(order: Order) -> str:
    """Сериализация заказа в JSON с поддержкой UUID и специальных типов"""
    def default_serializer(obj):
        if isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, ParameterType):
            return obj.value  # Предполагая, что ParameterType это enum
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    order_data = {
        "id": str(order['id']),
        "payload": order['payload'],
        "parameters": [
            {
                "name": param['name'],
                "type": param['type'].value if hasattr(param['type'], 'value') else str(param['type']),
                "value": param['value']
            }
            for param in order['parameters']
        ],
        "created_at": datetime.utcnow().isoformat()
    }
    
    return json.dumps(order_data, default=default_serializer)

# Дополнительные эндпоинты для работы с очередью
@order_router.get("/queue/stats")
async def get_queue_stats(redis: Redis = Depends(get_redis)) -> dict:
    """Получение статистики очереди"""
    try:
        queue_name = "orders_queue"
        queue_length = await redis.llen(queue_name)
        
        return {
            "queue_name": queue_name,
            "pending_orders": queue_length,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get queue stats: {str(e)}"
        )

@order_router.get("/{order_id}/status")
async def get_order_status(order_id: UUID, redis: Redis = Depends(get_redis)) -> dict:
    """Получение статуса заказа"""
    try:
        order_hash_key = f"order:{order_id}"
        order_data = await redis.hgetall(order_hash_key)
        
        if not order_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order {order_id} not found"
            )
        
        return {
            "order_id": order_id,
            "status": order_data.get('status', 'unknown'),
            "created_at": order_data.get('created_at'),
            "queue_position": order_data.get('queue_position')
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get order status: {str(e)}"
        )
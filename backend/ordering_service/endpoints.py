from fastapi import APIRouter, Depends
from uuid import uuid4, UUID
import redis
import json

from ordering_service.schemas import PlaceOrder
from entities.order import Order

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
ORDER_QUEUE_KEY = "order_queue"

order_router = APIRouter(prefix="/orders")

def get_redis():
    return redis_client

@order_router.post("/") 
async def place_order(body: PlaceOrder, redis_client: redis.Redis = Depends(get_redis)) -> Order:
    order = Order(
        id=uuid4(),
        parameters=body.parameters,
        payload=body
    )
    
    order_dict = dict(order)
    
    redis_client.lpush(ORDER_QUEUE_KEY, json.dumps(order_dict))
    
    return order

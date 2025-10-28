from fastapi import FastAPI

from ordering_service.endpoints import order_router
from settings import settings

app = FastAPI()
app.include_router(order_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.order_service_host, port=settings.order_service_port, reload=True)
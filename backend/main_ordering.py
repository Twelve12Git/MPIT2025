from fastapi import FastAPI

from ordering_service.endpoints import order_router
from settings import SETTINGS

app = FastAPI()
app.include_router(order_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_ordering:app", host=SETTINGS.APP_HOST, port=SETTINGS.ORDER_SERVICE_PORT, reload=True)
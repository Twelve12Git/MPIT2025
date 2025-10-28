from fastapi import FastAPI

from worker_service.endpoints import worker_router
from settings import settings

app = FastAPI()
app.include_router(worker_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.worker_service_host, port=settings.worker_service_port, reload=True)
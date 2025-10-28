from fastapi import FastAPI

from worker_service.endpoints import worker_router
from settings import SETTINGS

app = FastAPI()
app.include_router(worker_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_worker:app", host=SETTINGS.APP_HOST, port=SETTINGS.WORKER_SERVICE_PORT, reload=True)
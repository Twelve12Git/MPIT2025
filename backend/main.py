from fastapi import FastAPI
from order_handling import router as order_router

app = FastAPI()
app.include_router(order_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
from fastapi import FastAPI
from app.router.user_router import user_router
from app.router.record_router import record_router
from app.router.dashboard_router import dashboard_router
import os

app = FastAPI(title="Finance Dashboard Backend")


app.include_router(user_router, prefix="/users")
app.include_router(record_router, prefix="/records")
app.include_router(dashboard_router, prefix="/dashboard")



@app.get("/")
def root():
    return {
        "message": "Finance Dashboard Backend is running 🚀"
    }
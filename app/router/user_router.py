from fastapi import APIRouter
from sqlalchemy import create_engine
from app.config import DatabaseDetails
from app.rq_rs.user_rq_rs import UserCreateRequest, UserResponse
from app.utils.user_utils import create_user

user_router = APIRouter()

@user_router.post("/create_user", response_model=UserResponse)
def create_user_api(data: UserCreateRequest) -> UserResponse:
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    response = create_user(engine, data)
    engine.dispose()
    return response
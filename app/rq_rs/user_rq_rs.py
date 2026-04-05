from pydantic import BaseModel
from app.constants.status import Status

class UserCreateRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str

class UserResponse(BaseModel):
    status: Status
    user_id: int | None = None
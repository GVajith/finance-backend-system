from pydantic import BaseModel

class Status(BaseModel):
    status: bool
    message: str
from pydantic import BaseModel
from typing import Optional, List, Dict
from app.constants.status import Status
from typing import Literal

class RecordCreateRequest(BaseModel):
    user_id: int
    amount: float
    type: Literal["income", "expense"]
    category: str
    notes: Optional[str] = None


class RecordFetchRequest(BaseModel):
    user_id: int
    type: Optional[str] = None
    category: Optional[str] = None



class RecordUpdateRequest(BaseModel):
    user_id: int
    record_id: int
    amount: Optional[float] = None
    category: Optional[str] = None
    notes: Optional[str] = None



class RecordDeleteRequest(BaseModel):
    user_id: int
    record_id: int


class RecordResponse(BaseModel):
    status: Status
    data: Optional[List[Dict]] = []
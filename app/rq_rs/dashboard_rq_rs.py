from pydantic import BaseModel
from typing import Optional, List, Dict
from app.constants.status import Status


class DashboardRequest(BaseModel):
    user_id: int


class DashboardResponse(BaseModel):
    status: Status
    data: Optional[Dict] = {}
from fastapi import APIRouter
from sqlalchemy import create_engine
from app.config import DatabaseDetails
from app.rq_rs.record_rq_rs import *
from app.utils.record_utils import *



record_router = APIRouter()



@record_router.post("/create_record", response_model=RecordResponse)
def create_record_api(data: RecordCreateRequest) -> RecordResponse:
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    response = create_record(engine, data)
    engine.dispose()
    return response



@record_router.post("/fetch_records", response_model=RecordResponse)
def fetch_records_api(data: RecordFetchRequest) -> RecordResponse:
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    response = fetch_records(engine, data)
    engine.dispose()
    return response



@record_router.put("/update_record", response_model=RecordResponse)
def update_record_api(data: RecordUpdateRequest) -> RecordResponse:
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    response = update_record(engine, data, data.user_id)
    engine.dispose()
    return response



@record_router.delete("/delete_record", response_model=RecordResponse)
def delete_record_api(data: RecordDeleteRequest) -> RecordResponse:
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    response = delete_record(engine, data.record_id, data.user_id)
    engine.dispose()
    return response
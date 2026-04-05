from sqlalchemy import Table, MetaData, insert, select, update, delete, and_
from sqlalchemy.engine import Engine
from datetime import datetime
from app.models import tables
from app.rq_rs.record_rq_rs import *
from app.constants.status import Status
from app.config import DatabaseDetails
from app.utils.auth_utils import get_user_role

def create_record(engine: Engine, request: RecordCreateRequest) -> RecordResponse:
    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    record_table = Table(tables.RECORDS, metadata, autoload_with=engine)
    user_table = Table(tables.USERS, metadata, autoload_with=engine)

    try:
        with engine.begin() as conn:

            role = get_user_role(conn, user_table, request.user_id)

            if role != "admin":
                return RecordResponse(
                    status=Status(status=False, message="Only admin can create records"),
                    data=[]
                )

            result = conn.execute(
                insert(record_table).values(
                    user_id=request.user_id,
                    amount=request.amount,
                    type=request.type,
                    category=request.category,
                    notes=request.notes,
                    date=datetime.utcnow()
                )
            )

            return RecordResponse(
                status=Status(status=True, message="Record created successfully"),
                data=[{"record_id": result.inserted_primary_key[0]}]
            )

    except Exception as e:
        return RecordResponse(
            status=Status(status=False, message=str(e)),
            data=[]
        )


def fetch_records(engine: Engine, request: RecordFetchRequest) -> RecordResponse:
    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    record_table = Table(tables.RECORDS, metadata, autoload_with=engine)
    user_table = Table(tables.USERS, metadata, autoload_with=engine)

    try:
        with engine.begin() as conn:

            role = get_user_role(conn, user_table, request.user_id)

            if role not in ["admin", "analyst"]:
                return RecordResponse(
                    status=Status(status=False, message="Access denied"),
                    data=[]
                )

            conditions = [record_table.c.user_id == request.user_id]

            if request.type:
                conditions.append(record_table.c.type == request.type)

            if request.category:
                conditions.append(record_table.c.category == request.category)

            query = select(record_table).where(and_(*conditions))
            result = conn.execute(query).fetchall()

            if not result:
                return RecordResponse(
                    status=Status(status=False, message="No items fetched"),
                    data=[]
                )

            data = [dict(row._mapping) for row in result]

            return RecordResponse(
                status=Status(status=True, message="Records fetched successfully"),
                data=data
            )

    except Exception as e:
        return RecordResponse(
            status=Status(status=False, message=str(e)),
            data=[]
        )


def update_record(engine: Engine, request: RecordUpdateRequest, user_id: int) -> RecordResponse:
    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    record_table = Table(tables.RECORDS, metadata, autoload_with=engine)
    user_table = Table(tables.USERS, metadata, autoload_with=engine)

    try:
        with engine.begin() as conn:

            role = get_user_role(conn, user_table, user_id)

            if role != "admin":
                return RecordResponse(
                    status=Status(status=False, message="Only admin can update records"),
                    data=[]
                )

            update_values = {}

            if request.amount is not None:
                update_values["amount"] = request.amount

            if request.category is not None:
                update_values["category"] = request.category

            if request.notes is not None:
                update_values["notes"] = request.notes

            result = conn.execute(
                update(record_table)
                .where(record_table.c.id == request.record_id)
                .values(**update_values)
            )

            if result.rowcount == 0:
                return RecordResponse(
                    status=Status(status=False, message="No record found"),
                    data=[]
                )

            return RecordResponse(
                status=Status(status=True, message="Record updated successfully"),
                data=[]
            )

    except Exception as e:
        return RecordResponse(
            status=Status(status=False, message=str(e)),
            data=[]
        )

def delete_record(engine: Engine, record_id: int, user_id: int) -> RecordResponse:
    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    record_table = Table(tables.RECORDS, metadata, autoload_with=engine)
    user_table = Table(tables.USERS, metadata, autoload_with=engine)

    try:
        with engine.begin() as conn:

            role = get_user_role(conn, user_table, user_id)

            if role != "admin":
                return RecordResponse(
                    status=Status(status=False, message="Only admin can delete records"),
                    data=[]
                )

            result = conn.execute(
                delete(record_table).where(record_table.c.id == record_id)
            )

            if result.rowcount == 0:
                return RecordResponse(
                    status=Status(status=False, message="No record found"),
                    data=[]
                )

            return RecordResponse(
                status=Status(status=True, message="Record deleted successfully"),
                data=[]
            )

    except Exception as e:
        return RecordResponse(
            status=Status(status=False, message=str(e)),
            data=[]
        )
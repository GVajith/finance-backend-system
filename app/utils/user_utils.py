from sqlalchemy import Table, MetaData, insert, select, or_
from sqlalchemy.engine import Engine
from app.models import tables
from app.rq_rs.user_rq_rs import UserCreateRequest, UserResponse
from app.constants.status import Status
from app.config import DatabaseDetails


def create_user(engine: Engine, request: UserCreateRequest) -> UserResponse:
    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    user_table = Table(tables.USERS, metadata, autoload_with=engine)

    try:
        with engine.begin() as conn:


            existing_query = select(user_table.c.id).where(
                or_(
                    user_table.c.email == request.email,
                    user_table.c.name == request.name
                )
            )
            existing_user = conn.execute(existing_query).fetchone()

            if existing_user:
                return UserResponse(
                    status=Status(
                        status=False,
                        message="User with same email or username already exists"
                    ),
                    user_id=None
                )

            result = conn.execute(
                insert(user_table).values(
                    name=request.name,
                    email=request.email,
                    password=request.password,
                    role=request.role,
                    is_active=True
                )
            )

            return UserResponse(
                status=Status(status=True, message="User created successfully"),
                user_id=result.inserted_primary_key[0]
            )

    except Exception as e:
        return UserResponse(
            status=Status(status=False, message=f"Error: {str(e)}"),
            user_id=None
        )
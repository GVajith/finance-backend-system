from sqlalchemy import Table, MetaData, select, func
from sqlalchemy.engine import Engine
from app.models import tables
from app.rq_rs.dashboard_rq_rs import DashboardRequest, DashboardResponse
from app.constants.status import Status
from app.config import DatabaseDetails
from app.utils.auth_utils import get_user_role
from sqlalchemy import text
from sqlalchemy import text
def get_summary(engine, request):


    try:
        with engine.connect() as conn:

            query = text("""
                SELECT category, amount 
                FROM records 
                WHERE user_id = :user_id
            """)

            result = conn.execute(query, {"user_id": request.user_id})

            total_income = 0.0
            total_expense = 0.0

            for row in result:
                record_type = str(row[0]).strip().lower()
                amount = float(row[1])

                if record_type == "income":
                    total_income += amount
                elif record_type == "expense":
                    total_expense += amount

            return DashboardResponse(
                status=Status(status=True, message="Summary fetched successfully"),
                data={
                    "total_income": total_income,
                    "total_expense": total_expense,
                    "net_balance": total_income - total_expense
                }
            )

    except Exception as e:
        return DashboardResponse(
            status=Status(status=False, message=f"Error: {str(e)}"),
            data={}
        )
def get_category_totals(engine: Engine, request: DashboardRequest) -> DashboardResponse:
    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    record_table = Table(tables.RECORDS, metadata, autoload_with=engine)
    user_table = Table(tables.USERS, metadata, autoload_with=engine)

    try:
        with engine.begin() as conn:

            role = get_user_role(conn, user_table, request.user_id)

            if role not in ["admin", "analyst", "viewer"]:
                return DashboardResponse(
                    status=Status(status=False, message="Access denied"),
                    data={}
                )

            query = select(
                record_table.c.category,
                func.sum(record_table.c.amount).label("total")
            ).where(
                record_table.c.user_id == request.user_id
            ).group_by(record_table.c.category)

            result = conn.execute(query).fetchall()

            data = [
                {"category": row.category, "total": row.total}
                for row in result
            ]

            return DashboardResponse(
                status=Status(status=True, message="Category totals fetched"),
                data={"categories": data}
            )
    except Exception as e:
        return DashboardResponse(
            status=Status(status=False, message=str(e)),
            data={}
        )
def get_recent_activity(engine: Engine, request: DashboardRequest) -> DashboardResponse:
    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    record_table = Table(tables.RECORDS, metadata, autoload_with=engine)
    user_table = Table(tables.USERS, metadata, autoload_with=engine)

    try:
        with engine.begin() as conn:

            role = get_user_role(conn, user_table, request.user_id)

            if role not in ["admin", "analyst", "viewer"]:
                return DashboardResponse(
                    status=Status(status=False, message="Access denied"),
                    data={}
                )

            query = select(record_table).where(
                record_table.c.user_id == request.user_id
            ).order_by(
                record_table.c.date.desc()
            ).limit(5)

            result = conn.execute(query).fetchall()

            data = [dict(row._mapping) for row in result]

            return DashboardResponse(
                status=Status(status=True, message="Recent activity fetched"),
                data={"recent": data}
            )

    except Exception as e:
        return DashboardResponse(
            status=Status(status=False, message=str(e)),
            data={}
        )


def get_monthly_trends(engine: Engine, request: DashboardRequest) -> DashboardResponse:
    metadata = MetaData(schema=DatabaseDetails.DEFAULT_SCHEMA)
    record_table = Table(tables.RECORDS, metadata, autoload_with=engine)
    user_table = Table(tables.USERS, metadata, autoload_with=engine)

    try:
        with engine.begin() as conn:

            role = get_user_role(conn, user_table, request.user_id)

            if role not in ["admin", "analyst", "viewer"]:
                return DashboardResponse(
                    status=Status(status=False, message="Access denied"),
                    data={}
                )

            query = select(
                func.strftime('%Y-%m', record_table.c.date).label("month"),
                func.sum(record_table.c.amount).label("total")
            ).where(
                record_table.c.user_id == request.user_id
            ).group_by("month")

            result = conn.execute(query).fetchall()

            data = [
                {"month": row.month, "total": row.total}
                for row in result
            ]

            return DashboardResponse(
                status=Status(status=True, message="Monthly trends fetched"),
                data={"trends": data}
            )

    except Exception as e:
        return DashboardResponse(
            status=Status(status=False, message=str(e)),
            data={}
        )
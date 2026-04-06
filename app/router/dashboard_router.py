from fastapi import APIRouter
from sqlalchemy import create_engine
from app.config import DatabaseDetails
from app.rq_rs.dashboard_rq_rs import DashboardRequest, DashboardResponse
from app.services.dashboard_service import *

dashboard_router = APIRouter()


@dashboard_router.post("/summary", response_model=DashboardResponse)
def summary_api(data: DashboardRequest) -> DashboardResponse:
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    response = get_summary(engine, data)
    engine.dispose()
    return response


@dashboard_router.post("/category", response_model=DashboardResponse)
def category_api(data: DashboardRequest) -> DashboardResponse:
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    response = get_category_totals(engine, data)
    engine.dispose()
    return response


@dashboard_router.post("/recent", response_model=DashboardResponse)
def recent_api(data: DashboardRequest) -> DashboardResponse:
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    response = get_recent_activity(engine, data)
    engine.dispose()
    return response


@dashboard_router.post("/trends", response_model=DashboardResponse)
def trends_api(data: DashboardRequest) -> DashboardResponse:
    engine = create_engine(DatabaseDetails.CONNECTION_STRING)
    response = get_monthly_trends(engine, data)
    engine.dispose()
    return response
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Index
)
from datetime import datetime
from config import DatabaseDetails
from models import tables

engine = create_engine(DatabaseDetails.CONNECTION_STRING)
metadata = MetaData()

users = Table(
    tables.USERS,
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("email", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
    Column("role", String, nullable=False),  # viewer / analyst / admin
    Column("is_active", Boolean, default=True),
    Column("created_at", DateTime, default=datetime.utcnow),
)


records = Table(
    tables.RECORDS,
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("amount", Float, nullable=False),
    Column("type", String, nullable=False),  # income / expense
    Column("category", String, nullable=False),
    Column("notes", String),
    Column("date", DateTime, default=datetime.utcnow),
    Column("created_at", DateTime, default=datetime.utcnow),
)


Index("idx_user_id", records.c.user_id)
Index("idx_date", records.c.date)
Index("idx_category", records.c.category)


metadata.create_all(engine)

print("✅ All tables created successfully")
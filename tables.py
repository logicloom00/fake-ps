from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from models import QueryType, OperationStatus, SystemState
from database import Base


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    operation_id = Column(String, index=True)
    provider = Column(String)
    operation_type = Column(String)
    query_type = Column(Enum(QueryType))
    status = Column(Enum(OperationStatus), nullable=True)
    system_state = Column(Enum(SystemState), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

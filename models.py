import enum
from pydantic import BaseModel


# Define your database model
class OperationStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    DECLINE = "DECLINE"
    FAILED = "FAILED"


class SystemState(str, enum.Enum):
    NORMAL = "NORMAL"
    OVERLOADING = "OVERLOADING"
    FAILING = "FAILING"
    UNAVAILABLE = "UNAVAILABLE"
    RECOVERING = "RECOVERING"


class QueryType(str, enum.Enum):
    INTERMEDIATE = "INTERMEDIATE"
    FINAL = "FINAL"


class CreateOperationRequest(BaseModel):
    operation_id: str
    provider: str
    operation_type: str


class CheckOperationRequest(BaseModel):
    pass
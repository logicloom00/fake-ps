from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import random

from models import CreateOperationRequest, SystemState, QueryType, OperationStatus
from tables import Operation
from database import SessionLocal, Base, engine
from utils import get_system_state

app = FastAPI()
# Create tables
Base.metadata.create_all(bind=engine)


@app.post("/operations")
def create_operation(request: CreateOperationRequest):
    db = SessionLocal()
    try:
        count_operation_created = db.query(Operation).count()

        operation = Operation(
            operation_id=request.operation_id,
            provider=request.provider,
            operation_type=request.operation_type,
            query_type=QueryType.INTERMEDIATE,
        )
        db.add(operation)
        db.commit()
        # db.refresh(operation)
    finally:
        db.close()
    
    response_data = {
        "query_type": operation.query_type,
        "system_state": get_system_state(count_operation_created),
        "operation_id": operation.operation_id,
        "provider": operation.operation_type,
        "operation_type": operation.operation_type
    }
    return JSONResponse(content=response_data)


@app.get("/operations/{operation_id}/check")
def check_operation(operation_id: str):
    db = SessionLocal()
    try:
        operation = db.query(Operation).filter(Operation.operation_id == operation_id).first()
        
        if not operation:
            raise HTTPException(status_code=404, detail="Operation not found")
        
        count_operation_created = db.query(Operation).count()
        
        # Simulate status based on system state
        system_current_state = get_system_state(count_operation_created)
        if operation.status is None:
            if system_current_state == SystemState.NORMAL:
                if operation.created_at + timedelta(seconds=random.randint(2, 5)) < datetime.utcnow():
                    operation.status = OperationStatus.SUCCESS
                    operation.query_type = QueryType.FINAL
                else:
                    operation.status = None
            elif system_current_state == SystemState.OVERLOADING:
                if operation.created_at + timedelta(seconds=random.randint(15, 20)) < datetime.utcnow():
                    operation.status = random.choice([OperationStatus.SUCCESS, OperationStatus.DECLINE])
                    operation.query_type = QueryType.FINAL
                else:
                    operation.status = None
            elif system_current_state == SystemState.FAILING:
                if operation.created_at + timedelta(seconds=random.randint(1, 3)) < datetime.utcnow():
                    operation.status = OperationStatus.FAILED
                    operation.query_type = QueryType.FINAL
                else:
                    operation.status = None
            elif system_current_state == SystemState.UNAVAILABLE:
                operation.status = None
            elif system_current_state == SystemState.RECOVERING:
                if operation.created_at + timedelta(seconds=random.randint(5, 10)) < datetime.utcnow():
                    operation.status = random.choice([OperationStatus.SUCCESS, OperationStatus.DECLINE])
                    operation.query_type = QueryType.FINAL
                else:
                    operation.status = None
            db.commit()
    finally:
        db.close()
    
    response_data = {
        "query_type": operation.query_type,
        "system_state": system_current_state,
        "status": operation.status,
        "operation_id": operation.operation_id,
        "provider": operation.provider,
        "operation_type": operation.operation_type
    }
    return JSONResponse(content=response_data)


if __name__ == '__main__':
    count_operation_created = 0
    uvicorn.run("main:app", host="0.0.0.0", port=8080)

from fastapi import FastAPI, HTTPException
from database import create_table, save_monitor, get_monitors, check_in
from pydantic import BaseModel, Field



app = FastAPI()
create_table()

class MonitorCreate(BaseModel):
    interval_seconds: int = Field(gt=0)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/monitors")
def create_monitor(monitor: MonitorCreate):

    monitor_id, deadline = save_monitor(monitor.interval_seconds)

    return {
        "id": monitor_id,
        "interval_seconds": monitor.interval_seconds,
        "deadline": deadline
    }

@app.get("/monitors")
def list_monitors():

    monitor_list = get_monitors()
    
    return monitor_list

@app.post("/monitors/{monitor_id}/check-in")
def check_in_monitor(monitor_id: int):

    new_deadline = check_in(monitor_id)

    if new_deadline is None:
        raise HTTPException(
            status_code=404,
            detail="Monitor not found"
        )

    return {
        "id": monitor_id,
        "message": "Check-in successful",
        "new_deadline": new_deadline
    }
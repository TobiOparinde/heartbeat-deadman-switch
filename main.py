from fastapi import FastAPI
from database import create_table, save_monitor
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
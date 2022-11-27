from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import pytz

utc=pytz.UTC
logger = logging.getLogger(__name__)
data_store = []
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
app = FastAPI()


class Reservation(BaseModel):
    reserved_for: str
    reserved_by: str
    start: datetime
    end: datetime


def check_if_reservation_overlaps(item):
    for ds in data_store:
        ds.start = ds.start.replace(tzinfo=utc)
        ds.end = ds.end.replace(tzinfo=utc)
        if ds.start >= item.end >= ds.end:
            return True, item
        if ds.start <= item.start <= ds.end:
            return True, item
    return False, None


def check_and_remove_if_exist_reservation(name):
    for item in data_store:
        if item.reserved_for == name:
            data_store.remove(item)


@app.delete("/delete/{reserved_for}")
async def delete_reservation(reserved_for):
    check_and_remove_if_exist_reservation(reserved_for)
    return {"ok": True}


@app.post("/create")
async def create_reservation(item: Reservation):
    overlap, overlapping_item = check_if_reservation_overlaps(item)

    if overlap:
        raise HTTPException(status_code=400, detail=f"Sorry {item.reserved_by}, overlapping with {overlapping_item.reserved_for}")
    else:
        data_store.append(item)
    return item


@app.get("/show")
async def get_reservation():
    return data_store

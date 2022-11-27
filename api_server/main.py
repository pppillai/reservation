from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

data_store = []
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
app = FastAPI()


def check_if_reservation_overlaps(start, end):
    for item in data_store:
        if item['end_datetime'] >= end >= item['start_datetime']:
            return True, item
        if item['start_datetime'] <= start <= item['end_datetime']:
            return True, item
    return False, None


def check_and_remove_if_exist_reservation(name):
    for item in data_store:
        if item['reserved_for'] == name:
            data_store.remove(item)


@app.delete("/delete/{reserved_for}")
async def delete_reservation(reserved_for):
    check_and_remove_if_exist_reservation(reserved_for)
    return {"ok": True}


@app.post("/create")
async def create_reservation(reserved_for, reserved_by, start_datetime, end_datetime):
    try:
        start = datetime.strptime(start_datetime, DATE_FORMAT)
        end = datetime.strptime(end_datetime, DATE_FORMAT)
    except ValueError as e:
        raise HTTPException(status_code=404, detail="Please use date time in %Y-%m-%dT%H:%M:%SZ format")

    overlap, item = check_if_reservation_overlaps(start, end)

    if overlap:
        msg = f"Sorry, {reserved_by} Overlapping with existing reservation {item['reserved_by']}"
        raise HTTPException(status_code=404, detail=msg)
    else:
        reservation = {
            "reserved_for": reserved_for,
            "reserved_by": reserved_by,
            "start_datetime": start,
            "end_datetime": end
        }
        data_store.append(reservation)
    return reservation


@app.get("/show")
async def get_reservation():
    return data_store

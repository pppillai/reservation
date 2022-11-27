from datetime import datetime
from fastapi import FastAPI, HTTPException

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


@app.post("/create")
async def root(reserved_for, reserved_by, start_datetime, end_datetime):
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
async def root():
    return data_store

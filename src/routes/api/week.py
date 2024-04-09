from flask import redirect, url_for, request, jsonify
import calendar, datetime
from models import OperatorManager, Operator, EventManager, Event
from utils import get_week_days

def is_valid_date(year:int, month:int, day:int):
    try:
        datetime(year, month, day)
        return True
    except: return False

def get_week():
    #structure of post request: "operator":"operatorID", "day":"dayNumber", "month":"monthNumber", "year":"yearNumber"
    data = request.json
    operator = OperatorManager.get(data["operator"])
    
    if not Operator: return None #TODO: add error to user
    if not is_valid_date(data["year"], data["month"], data["day"]): return "Invalid Date", 400
    if datetime(data["year"], data["month"], data["day"]) < datetime.now():
        return "Invalid date", 400

    response = []
    for date in get_week_days(day=data["day"], month=data["month"], year=data["year"]):
        dateStr = f"{date[2]}-{date[1]:02d}-{date[0]:02d}"
        events = operator.getEventsByDate(dateStr) #returns a list of events in that day
        
        response.append({
            "date":date,
            "events":len(events)
        })

        for event in events:
            time_span = event.getTimeSpan()
            response.append({
                "start_hour": time_span[0],
                "end_hour"  : time_span[1]
            })
    
    return jsonify(response)
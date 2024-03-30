from flask import redirect, url_for, request, jsonify
import calendar
from models import OperatorManager, Operator, EventManager, Event

def get_month():
    #structure of post request: "operator":"operatorID", "month":"monthNumber"
    data = request.json
    operator = OperatorManager.get(data["operator"])
    
    if not Operator: return None #TODO: add error to user

    response = []
    for day in range(calendar.monthrange(year=2023, month=data["month"])):
        events = operator.getEventsByDay(day=day) #returns a list of events in that day
        
        response.append({
            "day":day,
            "events":len(events)
        })
    
    return jsonify(response)
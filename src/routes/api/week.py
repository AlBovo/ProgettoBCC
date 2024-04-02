from flask import redirect, url_for, request, jsonify
import calendar
from models import OperatorManager, Operator, EventManager, Event
from utils import get_week_days

def get_month():
    #structure of post request: "operator":"operatorID", "day":"dayNumber", "month":"monthNumber", "year":"yearNumber"
    data = request.json
    operator = OperatorManager.get(data["operator"])
    
    if not Operator: return None #TODO: add error to user

    response = []
    for day in range(get_week_days(day=data["day"], month=data["month"], year=data["year"])):
        events = operator.getEventsByDay(day=day) #returns a list of events in that day
        
        response.append({
            "day":day,
            "events":len(events)
        })
    
    return jsonify(response)
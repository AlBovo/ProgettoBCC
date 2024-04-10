from flask import redirect, url_for, request, jsonify
from models import OperatorManager
import datetime

def get_day():
    
    # Post request with: "date":YYYY-MM-GG, "operator":operatorId

    data = request.json()

    if not data["date"]: return "Invalid date", 400
    if not data["operator"]: return "Invalid operator", 400

    #check invalid date (date is in the past)
    if datetime(data["date"][:4], data["date"][5:7], data["date"][8:]) < datetime.now():
        return "Invalid Date", 400

    operator = OperatorManager.get(data["operator"])
    events = operator.getEventsByDate(data["date"])

    response = []

    for event in events:
        response.append({
            "start_hour": event.getTimeSpan()[0],
            "end_hour"  : event.getTimeSpan()[1]
        })
    
    return jsonify(response), 200

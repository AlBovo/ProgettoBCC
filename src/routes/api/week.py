from flask import request, jsonify
import datetime
from models import OperatorManager, Operator
from utils import get_week_days, is_valid_date

def get_week():
    #structure of post request: "operator":"operatorID", "day":"dayNumber", "month":"monthNumber", "year":"yearNumber"
    data = request.json
    operator = OperatorManager.get(data["operator"])
    
    if not Operator:
        return jsonify({'error': 'Operator not found'}), 400
    if not is_valid_date(f'{data["year"]}-{data["month"]}-{data["day"]}'): 
        return jsonify({'error': 'Invalid format date'}), 400
    if datetime(data["year"], data["month"], data["day"]) < datetime.now():
        return jsonify({'error': 'Invalid date'}), 400

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
    
    return jsonify(response), 200
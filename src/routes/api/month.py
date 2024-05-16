from flask import request, jsonify
from models import OperatorManager
import calendar, datetime

def get_month():
    """
    Retrieves the number of events for each day in a given month and year.

    Returns:
        A JSON response containing the number of events for each day in the specified month and year.
    """
    data = request.json

    if not data.get("month", type=int) or not data.get("year", type=str):
        return jsonify({"error":"Missing parameters"}), 400
    if not isinstance(data["month"], int) or not isinstance(data["year"], str):
        return jsonify({"error":"Invalid parameters"}), 400
    
    if not data["month"] in range(1,13):
        return jsonify({"error":"Invalid month"}), 400
    
    if not data["year"] in range(datetime.now().year, datetime.now().year+2):
        return jsonify({"error":"Invalid year"}), 400
    
    if datetime(data["year"], data["month"], 1) < datetime(datetime.now().year, datetime.now().month, 1):
        return jsonify({'error': 'Invalid year or month'}), 400

    response = [0] * (calendar.monthrange(data["year"], data["month"])[1])
    i = 0
    
    while True:
        if not (operator := OperatorManager.get(i)):
            break
        
        i += 1
        for day in range(1, calendar.monthrange(data["year"], data["month"])[1]):
            date = f"{data['year']}-{data['month']:02d}-{day:02d}"
            events = operator.getEventsByDate(date) # returns a list of events in that day
            
            if events:
                response[day - 1] += len(events)
            else:
                break
        
    return jsonify(response), 200
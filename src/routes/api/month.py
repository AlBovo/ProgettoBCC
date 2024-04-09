from flask import request, jsonify
from models import OperatorManager, Operator
import calendar, datetime

def get_month():
    """
    Retrieves the number of events for each day in a given month for a specific operator.
    structure of post request: {"operator": operatorID, "month": monthNumber, "year": yearNumber}

    Returns:
        A JSON response containing the number of events for each day in the specified month.

    Raises:
        400: If the request is missing parameters or if the parameters are invalid.
        400: If the specified operator is not found.
        400: If the specified month is invalid.
    """
    data = request.json

    if not "operator" in data or not "month" in data:
        return jsonify({"error":"Missing parameters"}), 400
    if not isinstance(data["operator"], int) or not isinstance(data["month"], int):
        return jsonify({"error":"Invalid parameters"}), 400

    operator = OperatorManager.get(data["operator"])
    
    if not Operator: 
        return jsonify({"error":"Operator not found"}), 400
    
    if not data["month"] in range(1,13):
        return jsonify({"error":"Invalid month"}), 400
    
    if not data["year"] in range(datetime.now().year, datetime.now().year+2):
        return jsonify({"error":"Invalid year"}), 400
    
    if datetime(data["year"], data["month"], 1) < datetime(datetime.now().year, datetime.now().month, 1):
        return "Invalid year - month", 400

    response = []
    for day in range(1, calendar.monthrange(data["year"], data["month"])[1]):
        date = f"{data['year']}-{data['month']:02d}-{day:02d}"
        events = operator.getEventsByDate(date) # returns a list of events in that day
        
        response.append({
            "day":day,
            "events":len(events)
        })
    
    return jsonify(response), 200
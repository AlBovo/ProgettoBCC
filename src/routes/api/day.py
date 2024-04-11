from flask import request, jsonify
from models import OperatorManager
from datetime import datetime

def get_day():
    
    # Post request with: "date":YYYY-MM-GG, "operator":operatorId

    data = request.json()

    if not data["date"] or not data["operator"]: return jsonify({'error': 'Missing parameters'}), 400
    if not isinstance(data["date"], str): return jsonify({'error': 'Invalid date'}), 400
    if not isinstance(data["operator"], int): return jsonify({'error' : 'Invalid operator'}), 400

    #check invalid date (date is in the past)
    try:
        if datetime.strptime(data["date"], "%Y-%m-%d") < datetime.now():
            return jsonify({'error': 'Invalid date'}), 400
    except:
        return jsonify({'error': 'Invalid format date'}), 400
    
    operator = OperatorManager.get(data["operator"])
    events = operator.getEventsByDate(data["date"])

    response = []

    for event in events:
        response.append({
            "start_hour": event.getTimeSpan()[0],
            "end_hour"  : event.getTimeSpan()[1]
        })
    
    return jsonify(response), 200

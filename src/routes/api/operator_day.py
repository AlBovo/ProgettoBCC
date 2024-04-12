from flask import request, jsonify
from models import OperatorManager
from datetime import datetime
from utils import code_to_category

def get_operator_day():
    
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
        category = code_to_category(event.getCategory())
        timeSpan = event.getTimeSpan()

        response.append({
            "email"     : event.getUser().get_email(),
            "category"  : category,
            "start_hour": timeSpan[0],
            "end_hour"  : timeSpan[1]
        })
    
    return jsonify(response), 200

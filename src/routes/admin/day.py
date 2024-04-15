from flask import request, jsonify
from models import OperatorManager
from datetime import datetime
from utils import code_to_category

def get_operator_day():
    
    # Post request with: "operator":operatorId

    data = request.json()

    if not data["operator"]: return jsonify({'error': 'Missing parameters'}), 400
    if not isinstance(data["operator"], int): return jsonify({'error' : 'Invalid operator'}), 400
    
    operator = OperatorManager.get(data["operator"])
    response = []

    for event in operator.getAllEvents():
        category = code_to_category(event.getCategory())
        timeSpan = event.getTimeSpan()

        response.append({
            "email"     : event.getUser().get_email(),
            "category"  : category,
            "start_hour": timeSpan[0],
            "end_hour"  : timeSpan[1]
        })
    
    return jsonify(response), 200

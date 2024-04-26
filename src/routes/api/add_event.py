from flask_login import current_user
from flask import request, jsonify
from models import EventManager
import utils

def add_event():
    """
    Add an event to the system.

    This function retrieves the necessary parameters from the request JSON and performs validation checks.
    If the parameters are valid, the event is added to the system using the EventManager.addEvent method.
    If the event is added successfully, a success message is returned. Otherwise, an error message is returned.
    The start/end hours must be between 8:30 and 17:00, and the format should be HHMM.
    structure of post request: {"date": "YYYY-MM-DD", "start_hour": HHMM, "end_hour": HHMM, "operator_id": operatorId}
    
    Returns:
        A JSON response containing either a success message or an error message.
    """
    date = request.json.get('date', None)
    start_hour = request.json.get('start_hour', None)
    end_hour = request.json.get('end_hour', None)
    category = request.json.get('category', None)
    operator_id = request.json.get('operator_id', None)
    user_id = current_user.get_id()
    
    if date == None or start_hour == None or end_hour == None or operator_id == None:
        return jsonify({'error': 'Missing parameters in request'}), 400
    if not isinstance(date, str) or not isinstance(start_hour, int) or not isinstance(end_hour, int) or not isinstance(operator_id, int):
        return jsonify({'error': 'Invalid parameter types in request'}), 400
    if start_hour >= end_hour:
        return jsonify({'error': 'Invalid time range, start hour must be before end hour'}), 400
    if start_hour < 830 or start_hour > 1700 or end_hour < 830 or end_hour > 1700:
        return jsonify({'error': 'Invalid time range, not in correct working range'}), 400
    if not utils.is_valid_date(date):
        return jsonify({'error': 'Invalid date format'}), 400
    
    if EventManager.addEvent(date, start_hour, end_hour, category, user_id, operator_id):
        return jsonify({'message': 'Event added successfully'}), 200
    else:
        return jsonify({'error': 'Invalid request, the event is not valid.'}), 404
from flask import request, jsonify
from flask_login import current_user
from models import EventManager

def delete_event():
    """
    Deletes an event based on the provided event ID.
    structure of post request: {"id": eventId}

    Returns:
        A JSON response containing either a success message or an error message.
    """
    id = request.json.get('id', None)
    
    if not id:
        return jsonify({'error': 'Event ID is required'}), 400
    
    if not isinstance(id, int):
        return jsonify({'error': 'Event ID must be an integer'}), 400
    
    if EventManager.deleteEvent(id, current_user.get_id()):
        return jsonify({'message': 'Event deleted successfully'}), 200
    else:
        return jsonify({'error': 'Event not found'}), 404
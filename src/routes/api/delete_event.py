from flask import request, jsonify
from flask_login import current_user
from models import EventManager

def delete_event():
    id = request.json.get('id', None)
    
    if not id:
        return jsonify({'error': 'Event ID is required'}), 400
    
    if EventManager.deleteEvent(id, current_user.get_id()):
        return jsonify({'message': 'Event deleted successfully'}), 200
    else:
        return jsonify({'error': 'Event not found'}), 404
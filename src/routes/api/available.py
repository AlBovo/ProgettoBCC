from flask import jsonify, request
from models import OperatorManager
import utils

def get_available():
    """
    Retrieves the available operators for a given date.

    Returns:
        A JSON response containing the available operators for the given date.
    """
    date = request.json.get('date', None)
    
    if not date:
        return jsonify({'error': 'Missing parameters in request'}), 400
    
    if not utils.is_valid_date(date):
        return jsonify({'error': 'Invalid date format'}), 400
        
    if utils.is_past_date(date):
        return jsonify({'error': 'Invalid date'}), 400

    response = OperatorManager.getAllAvailable(date)
    for i in response:
        response[i] = [OperatorManager.get(e).getInformations()[:2] for e in response[i]] # replace id with name and surname
    
    return jsonify(response), 200
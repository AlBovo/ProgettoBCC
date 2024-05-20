from flask import jsonify
from models import OperatorManager

def get_categories():
    """
    Retrieves all categories from the OperatorManager and returns them as a JSON response.

    Returns:
        A tuple containing the JSON response and the HTTP status code 200.
    """
    response = OperatorManager.getAllCategories()
    return jsonify(response), 200
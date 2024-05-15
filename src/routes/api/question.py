from flask import request, jsonify, redirect, url_for

def ask_quesstion():
    """
    Retrieves the question data of a specific ID.
    Structure of post request: {"question": questionID}
    
    Returns:
        A JSON response containing the data of the question.

    Raises:
        400: If the request is missing parameters or if the parameters are invalid.
        400: If the specified questions ID is not found.
    """

    #TODO: Implement this method
    return redirect(url_for('main.index')), 200
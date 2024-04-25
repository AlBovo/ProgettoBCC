from flask import request, jsonify
from models import EventManager
from datetime import datetime

def get_day():
    """
    Retrieves the events for a specific day and operator.
    Post request with: "date":YYYY-MM-GG
    
    Returns:
        A JSON response containing the start and end hours of each event for the specified day and operator.
        If there are any errors, an error message is returned with an appropriate status code.
    """
    
    data = request.json()

    if not data["date"]: return jsonify({'error': 'Missing parameters'}), 400
    if not isinstance(data["date"], str): return jsonify({'error': 'Invalid date'}), 400

    #check invalid date (date is in the past)
    try:
        if datetime.strptime(data["date"], "%Y-%m-%d") < datetime.now():
            return jsonify({'error': 'Invalid date'}), 400
    except:
        return jsonify({'error': 'Invalid format date'}), 400
    
    events = [
        {"start_hour": 0, "end_hour": 830}, # not avaible before 8:30 
        EventManager.getEventsByDate(data["date"]),
        {"start_hour": 1700, "end_hour": 2400} # not avaible after 17:00
    ]
    
    response = []
    
    hour, e = events[0]["end_hour"], 1
    while hour < events[-1]["start_hour"]:
        if hour == events[e]["start_hour"]:
            hour = events[e]["end_hour"]
            e += 1
        else:
            response.append({
                "start_hour": hour,
                "end_hour"  : (hour := (hour if hour % 100 < 60 else (hour // 100 + 1) * 100))
            })
            
    return jsonify(response), 200

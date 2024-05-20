from flask import flash, render_template, redirect, url_for
from flask_login import current_user
from models import OperatorManager
from utils import code_to_category
from datetime import datetime

def get_operator_day():    
    """
    Retrieves the events for the current operator and renders them on the operator.html template.

    Returns:
        The rendered operator.html template with the events for the current operator.
    """
  
    if not current_user.get_privilege():
        flash("You are not an operator at the moment", "error")
        return redirect(url_for('main.login'))
    
    operator = OperatorManager().get(current_user.get_id())
    
    response = []

    for event in operator.getAllEvents():
        category = code_to_category(event.getCategory())
        timeSpan = event.getTimeSpan()
        
        if datetime.now().date() != datetime.strptime(event.getDate(), "%Y-%m-%d").date():
            continue

        response.append({
            "date"      : event.getDate(),
            "email"     : event.getUser().get_email(),
            "category"  : category,
            "start_hour": f"{timeSpan[1] // 100}:{timeSpan[1] % 100}",
            "end_hour"  : f"{timeSpan[2] // 100}:{timeSpan[2] % 100}"
        })
    
    return render_template('operator.html', events=response)

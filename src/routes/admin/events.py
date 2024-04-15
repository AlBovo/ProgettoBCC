from flask import flash, render_template, redirect, url_for
from flask_login import current_user
from models import OperatorManager
from utils import code_to_category

def get_operator_day():    
    # Post request with: "operator":operatorId

    id = current_user.get_id()
    operator = OperatorManager.get(id)
    if operator == None:
        flash("You are not an operator at the moment", "error")
        return redirect(url_for('main.login'))
    
    response = []

    for event in operator.getAllEvents():
        category = code_to_category(event.getCategory())
        timeSpan = event.getTimeSpan()

        response.append({
            "date"      : event.getDate(),
            "email"     : event.getUser().get_email(),
            "category"  : category,
            "start_hour": timeSpan[0],
            "end_hour"  : timeSpan[1]
        })
    
    return render_template('operator.html', events=response)

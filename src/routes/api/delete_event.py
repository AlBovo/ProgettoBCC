from flask import redirect, url_for, request, flash
from flask_login import current_user
from models import EventManager

def delete_event():
    id = request.form.get('id')
    
    if not id:
        flash('Event ID is required', 'error')
        return redirect(url_for('main.dashboard'))
    
    if EventManager.delete_event(id, current_user.get_id()):
        flash('Event deleted successfully', 'success')
    else:
        flash('Event not found', 'error')
    
    return redirect(url_for('main.index')) # return data
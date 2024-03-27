from flask import redirect, url_for

def add_event():
    # TODO: add logic
    return redirect(url_for('main.index')) # return data
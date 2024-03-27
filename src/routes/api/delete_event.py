from flask import redirect, url_for

def delete_event():
    # TODO: add logic
    return redirect(url_for('main.index')) # return data
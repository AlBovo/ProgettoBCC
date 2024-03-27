from flask import redirect, url_for

def get_month():
    # TODO: add logic
    return redirect(url_for('main.index')) # return data
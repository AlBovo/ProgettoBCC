from flask import redirect, url_for

def question():
    # TODO: add logic
    return redirect(url_for('main.index')) # return data
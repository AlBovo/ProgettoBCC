from flask import redirect, url_for

def chatbot():
    return redirect(url_for('main.index')) # return data
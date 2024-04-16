from logging.handlers import RotatingFileHandler
from flask import Flask
from os import path
import logging

def init_app(app: Flask):
    app.config['LOG_PATH'] = path.join(app.config['LOG_DIR'], 'app.log')
    
    handler = RotatingFileHandler(
        app.config['LOG_PATH'], 
        maxBytes=2**20,
        backupCount=1,
        encoding="utf-8"
    )
    
    handler.setLevel(logging.INFO)
    
    handler.formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
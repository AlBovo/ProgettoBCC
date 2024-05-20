#!/usr/bin/env python3
from src import app
from flask import jsonify
import pytest, os, requests, datetime, json, calendar

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_month():
    
    URL_month = "http://localhost/api/month"

    data = {
        "operator": 1, #admin
        "year"    : datetime.now().year,
        "month"   : datetime.now().month
    }

    expected = []
    for day in range(1, calendar.monthrange(datetime.now().year, datetime.now().month)[1]):
        expected.append({
            "day":day,
            "events":0
        })
    
    expected = jsonify(expected)

    r = requests.post(URL_month, data=data, allow_redirects=True)
    assert r.json() == expected and r.status_code == 200

    pass

def test_invalid_month():
    URL_month = "http://localhost/api/month"

    data = {
        "operator": 1, #admin
        "year"    : datetime.now().year if datetime.now().month != 1 else datetime.now().year - 1,
        "month"   : datetime.now().month - 1 if datetime.now().month != 1 else 12 
    }

    r = requests.post(URL_month, data=data, allow_redirects=True)
    assert r.status_code == 400

    pass

def test_inexistent_month():
    URL_month = "http://localhost/api/month"

    data = {
        "operator": 1, #admin
        "year"    : datetime.now().year,
        "month"   : -1
    }

    r = requests.post(URL_month, data=data, allow_redirects=True)
    assert r.status_code == 400

    pass
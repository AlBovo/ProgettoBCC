#!/usr/bin/env python3
from src import app
import pytest, os, requests, datetime, json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_week():
    
    URL_week = "http://localhost/api/week"

    data = {
        "operator": 1, #admin
        "year"    : datetime.now().year,
        "month"   : datetime.now().month,
        "day"     : datetime.now().day
    }

    expected = json.loads({
        "month"   : f"{datetime.now().year:02d}-{datetime.now().month:02d}-{datetime.now().day:02d}",
        "events"  : 0
    })

    r = requests.post(URL_week, data=data, allow_redirects=True)
    assert r.json() == expected and r.status_code == 200

    pass
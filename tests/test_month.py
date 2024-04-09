#!/usr/bin/env python3
from src import app
import pytest, os, requests, datetime, json

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

    expected = json.loads({
        "month"   : datetime.now().month,
        "events"  : 0
    })

    r = requests.post(URL_month, data=data, allow_redirects=True)
    assert r.json() == expected and r.status_code == 200

    pass
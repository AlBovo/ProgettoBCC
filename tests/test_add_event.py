#!/usr/bin/env python3
from src import app
import pytest, os, requests

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

URL_addEvent = "http://localhost/api/add_event"
URL_register = "http://localhost/api/register"
URL_login = "http://localhost/api/login"

data = {
    "email": os.urandom(4).hex() + "@tests.com",
    "password": (password := os.urandom(8).hex()),
    "password_confirm": password
}

r = requests.post(URL_register, data=data, allow_redirects=True)
assert r.status_code == 200 and r.url == "http://localhost/login"
data.pop("password_confirm")
s = requests.Session()
r = s.post(URL_login, data=data, allow_redirects=True)
assert r.status_code == 200 and r.url == "http://localhost/dashboard"

def test_add_event_Valid():
    r = s.post(URL_addEvent, json={'date' : '2024-12-31', 'start_hour' : 830, 'end_hour' : 1700, 'operator_id' : 1}) # valid
    assert r.status_code == 200
    
def test_add_event_InvalidStartHour():
    r = s.post(URL_addEvent, json={'date' : '2024-12-31', 'start_hour' : 0, 'end_hour' : 1700, 'operator_id' : 1}) # invalid start_hour
    assert r.status_code == 400
    
def test_add_event_InvalidEndHour():
    r = s.post(URL_addEvent, json={'date' : '2024-12-31', 'start_hour' : 830, 'end_hour' : 0, 'operator_id' : 1}) # invalid end_hour
    assert r.status_code == 400

def test_add_event_InvalidDate():
    r = s.post(URL_addEvent, json={'date' : '202f12-31', 'start_hour' : 830, 'end_hour' : 1700, 'operator_id' : 0}) # invalid date
    assert r.status_code == 400

def test_add_event_EventAlreadyExists():
    r = s.post(URL_addEvent, json={'date' : '2024-12-31', 'start_hour' : 830, 'end_hour' : 1700, 'operator_id' : 1}) # event already exists
    assert r.status_code == 404

def test_add_event_OperatorDoesNotExist():
    r = s.post(URL_addEvent, json={'date' : '2024-12-31', 'start_hour' : 830, 'end_hour' : 1700, 'operator_id' : 2}) # operator does not exist
    assert r.status_code == 404

def test_add_event_MissingParameters():
    r = s.post(URL_addEvent, json={'date' : '2024-12-31', 'start_hour' : 830, 'end_hour' : 1700}) # missing parameters
    assert r.status_code == 400

def test_add_event_InvalidRangeHour():
    r = s.post(URL_addEvent, json={'date' : '2024-12-31', 'start_hour' : 1700, 'end_hour' : 830, 'operator_id' : 1}) # invalid range hour
    assert r.status_code == 400
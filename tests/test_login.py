#!/usr/bin/env python3
from src import app
import pytest, os, requests

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_login():
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
    r = requests.post(URL_login, data=data, allow_redirects=True)
    assert r.status_code == 200 and r.url == "http://localhost/dashboard"
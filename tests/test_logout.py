#!/usr/bin/env python3
from src import app
import requests, pytest, os

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
        
def test_logout():
    URL_register = "http://localhost/api/register"
    URL_login = "http://localhost/api/login"
    s = requests.Session()
    
    data = {
        "email": os.urandom(4).hex() + "@tests.com",
        "password": (password := os.urandom(8).hex()),
        "password_confirm": password
    }

    r = s.post(URL_register, data=data, allow_redirects=True)
    assert r.status_code == 200 and r.url == "http://localhost/login"

    data.pop("password_confirm")
    r = s.post(URL_login, data=data, allow_redirects=True)
    assert r.status_code == 200 and r.url == "http://localhost/dashboard"
    
    r = s.get("http://localhost/api/logout", allow_redirects=True)
    assert r.status_code == 200 and r.url == "http://localhost/"
    
    r = s.get("http://localhost/dashboard", allow_redirects=True)
    assert r.status_code == 200 and r.url.startswith("http://localhost/login") # redirected to login page
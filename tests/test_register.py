#!/usr/bin/env python3
import requests, os, pytest

@pytest.fixture
def test() -> requests.Response:
    URL_register = "http://localhost/api/register"
    URL_login = "http://localhost/api/login"

    data = {
        "email": (email := os.urandom(4).hex() + "@tests.com"),
        "password": (password := os.urandom(8).hex()),
        "password_confirm": password
    }

    r = requests.post(URL_register, data=data, allow_redirects=True)
    assert r.status_code == 200 and r.url == "http://localhost/login"

    data.pop("password_confirm")
    r = requests.post(URL_login, data=data, allow_redirects=True)
    print(r.content)
    assert r.status_code == 200 and r.url == "http://localhost/dashboard"
    return r

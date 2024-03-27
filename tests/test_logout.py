#!/usr/bin/env python3
import tests.test_register as test_register, requests, pytest

@pytest.fixture
def test() -> None:
    r = test_register.test()
    assert r.cookies.get_dict() not in [{}, None]
    
    r = requests.get("http://localhost/logout", allow_redirects=True)
    assert r.cookies.get_dict() == {}
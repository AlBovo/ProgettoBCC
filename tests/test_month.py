#!/usr/bin/env python3
from src import app
import pytest, os, requests

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_month():
    pass
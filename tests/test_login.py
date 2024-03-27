#!/usr/bin/env python3
import tests.test_register as test_register, pytest

@pytest.fixture
def test() -> None:
    test_register.test()
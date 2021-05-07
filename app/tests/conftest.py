import pytest
from flask import Flask
from ..app import app


@pytest.yield_fixture(scope='function')
def test_client(): 
    # and handling the context locals for you.
    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield testing_client 

    ctx.pop
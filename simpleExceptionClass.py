from flask import Flask
import pytest
import app

# The client() function retuns the value of testing the app with test_client() method
@pytest.fixture
def client():
    #Set app testing to True
    app.testing = True

    #Then we return the value of running the test_client() method on our app
    return app.app.test_client()

# The test_urls() function to test the web pages of the app individually with client() as input
def test_urls(client):
    # Defining r variable to test
    r = client.get('/')
    assert r.status_code == 200

    r = client.get('/home')
    assert r.status_code == 200

    r = client.get('/about')
    assert r.status_code == 200

    # second blueprint instance
    r = client.get('/create_post')
    assert r.status_code == 200

test_urls(client())

"""Test cases for the calculator application."""
import pytest
import json
import math
from FlaskCalculator import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_cosine_zero(client):
    """Test cosine of 0 radians should be 1."""
    response = client.post('/calculate',
                          data=json.dumps({'num1': 0, 'operation': 'cos'}),
                          content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert abs(data['result'] - 1.0) < 1e-10


def test_cosine_pi(client):
    """Test cosine of pi radians should be -1."""
    response = client.post('/calculate',
                          data=json.dumps({'num1': math.pi, 'operation': 'cos'}),
                          content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert abs(data['result'] - (-1.0)) < 1e-10


def test_cosine_pi_over_2(client):
    """Test cosine of pi/2 radians should be approximately 0."""
    response = client.post('/calculate',
                          data=json.dumps({'num1': math.pi / 2, 'operation': 'cos'}),
                          content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert abs(data['result']) < 1e-10


def test_cosine_invalid_input(client):
    """Test cosine with invalid input."""
    response = client.post('/calculate',
                          data=json.dumps({'num1': 'invalid', 'operation': 'cos'}),
                          content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'error' in data


def test_cosine_no_input(client):
    """Test cosine with no input."""
    response = client.post('/calculate',
                          data=json.dumps({'operation': 'cos'}),
                          content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 400
    assert 'error' in data


def test_add_still_works(client):
    """Test that addition still works after adding cosine."""
    response = client.post('/calculate',
                          data=json.dumps({'num1': 5, 'num2': 3, 'operation': 'add'}),
                          content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['result'] == 8


def test_divide_still_works(client):
    """Test that division still works after adding cosine."""
    response = client.post('/calculate',
                          data=json.dumps({'num1': 10, 'num2': 2, 'operation': 'divide'}),
                          content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['result'] == 5

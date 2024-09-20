import json
import pytest
from api.v1.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True  # Enable testing mode
    with app.test_client() as client:
        yield client
def test_add_book(client):
    data = {
        'title': 'The Alchemist',
        'publisher': 'HarperCollins',
        'category': 'Fiction',
    }
    response = client.post('/api/v1/add_book', json=data)
    assert response.status_code == 201
    assert response.json == {'book added': data}

def test_get_unavailable_books(client):
    response = client.get('/api/v1/unavailable_books')
    assert response.status_code == 200
    assert response.json == {'message': 'All books are available'}


# def test_remove_book(client):
#     response = client.delete('/api/v1/remove_book/4b16bfa4-da33-441c-a852-d8bc42952468')
#     assert response.status_code == 200
#     assert response.json == {'book removed': {'id': '4b16bfa4-da33-441c-a852-d8bc42952468', 'title': 'The Alchemist', 'publisher': 'HarperCollins', 'category': 'Fiction'}}

def test_get_users(client):
    response = client.get('/api/v1/get_users')
    assert response.status_code == 200
    assert response.json == {'message': [{'firstName': 'Dinobi1', 'lastName': 'Udeh', 'email': 'udehdinobi@gmail.com'}]}


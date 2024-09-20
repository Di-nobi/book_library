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
    assert response.json == {'message': [{'firstName': 'Dinobi1', 'lastName': 'Udeh', 'email': 'udehdinobi@gmail.com'}, {'email': 'udehdinobi@gmail.com', 'firstName': 'Dinobi2', 'lastName': 'Udeh'}]}

def test_get_unavailable_books(client):
    response = client.get('/api/v1/unavailable_books')
    assert response.status_code == 200
    expected_books = [
        {
            "category": "Fiction",
            "due_date": "2024-09-27",
            "id": "2c7a06c7-0b71-407e-bd7a-224f4ae6bc1e",
            "publisher": "HarperCollins",
            "title": "The Alchemist of Dinobi"
        },
        {
            "category": "Fiction",
            "due_date": "2024-09-27",
            "id": "b3a756b0-5db2-45df-bd55-f4e7d4e78e64",
            "publisher": "HarperCollins",
            "title": "The Alchemist of Dinobi22"
        },
        {
            "category": "Fiction",
            "due_date": "2024-09-27",
            "id": "492c4766-9fa5-4ace-8a1b-25c49544f0d7",
            "publisher": "HarperCollins",
            "title": "The Alchemist of Dinobi23"
        },
        {
            "category": "Fiction",
            "due_date": "2024-09-27",
            "id": "c334e869-80f7-4c0a-8ffb-dbe594dc11b7",
            "publisher": "HarperCollins",
            "title": "The Alchemist of Dinobi24"
        }
    ]
    actual_books = response.json['unavailable books']
    assert all(book in actual_books for book in expected_books)

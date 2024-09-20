import json
import pytest
from api.v1.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True  # Enable testing mode
    with app.test_client() as client:
        yield client


def test_get_book(client):
    response = client.get('/api/v1/book/4b16bfa4-da33-441c-a852-d8bc42952468')
    assert response.status_code == 200
    assert response.json == {'book': {'title': 'The Alchemist', 'publisher': 'HarperCollins', 'category': 'Fiction'}}

def test_get_available_books(client):
    response = client.get('/api/v1/available_books')
    assert response.status_code == 200
    expected_books = [
        {
            "category": "Fiction",
            "id": "4b16bfa4-da33-441c-a852-d8bc42952468",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "b41b2bd5-2710-4f32-8dfc-1457cf119f7e",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "e9be96f5-8230-4d86-b7e6-6fa40d98f9c8",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "309db14d-adc4-474c-9dfe-59371d9d7d42",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "39857c21-9670-4011-9e4b-659159cb8d4d",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "0421f3b1-4694-48b1-93d7-fe1309273c0b",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "27b42fc3-99e1-418d-a630-68832d8ab164",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "25685c04-3b6f-4d51-b77d-f5ed1c8ee2a2",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "10f246e2-275e-4457-85d8-8dff1b49b309",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "f73bed15-8504-4fdb-b3ee-a2dce9374227",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "94c57b82-29b3-4e2d-b794-b9826388ea66",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "860a1c2b-d9dd-4f79-b426-a8d36b6735b0",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "4f29d42b-d776-40ad-a893-d4e467f7c317",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "8c40f618-7492-431f-a757-8f79fb1a0fa4",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "d4d09557-5ee5-413f-9616-67c0a550e814",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "c8e65298-9fe9-4b0f-8cd0-c636d17e5dcf",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "08877a99-e6c3-4a3e-af5c-bc11ee9a701e",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "0481b26a-57d1-4e98-8a2e-2cec3acac319",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        },
        {
            "category": "Fiction",
            "id": "15778e98-3f4a-4f5c-b3cd-b385f0e92d3d",
            "publisher": "HarperCollins",
            "title": "The Alchemist"
        }
    ]
    actual_books = response.json['books']
    assert all(book in actual_books for book in expected_books)

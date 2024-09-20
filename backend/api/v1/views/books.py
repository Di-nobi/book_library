from flask import jsonify, request, redirect, abort
import requests
from api.v1.views import app_look
from database import storage


@app_look.route('/add_book', methods=['POST'])
def add_book():
    """Adds new books to the catalogue"""
    data = request.get_json()
    kwargs = {
        'title': data.get('title'),
        'publisher': data.get('publisher'),
        'category': data.get('category'),
        'available': True
    }
    if not kwargs['title'] or not kwargs['publisher'] or not kwargs['category']:
        return jsonify({'error': 'Missing required fields'}), 400
    book = storage.add_books(**kwargs)

    url = 'http://frontend:5001/api/v1/update_catalog'
    try:
        requests.post(url, json={
            'id': book.id,
            'title': book.title,
            'publisher': book.publisher,
            'category': book.category,
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Could not notify the frontend {e}'}), 500
    
    book_data = {
        'title': book.title,
        'publisher': book.publisher,
        'category': book.category
    }
    return jsonify({'book added': book_data }), 201

@app_look.route('/remove_book/<book_id>', methods=['DELETE'])
def remove_book(book_id):
    """Removes a book from the catalogue"""
    book = storage.get_book_by_id(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    storage.delete(book)
    storage.save()
    url = 'http://frontend:5001/remove_catalog'
    try:
        requests.delete(url, json={'book_id': book_id})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Could not notify the frontend {e}'}), 500
    return jsonify({'book removed': book.to_dict()}), 200

@app_look.route('/get_users', methods=['GET'])
def get_users():
    """Retrieves all users in the library"""
    users = storage.get_users()
    user_list = []
    for user in users:
        data = {
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email
        }
        user_list.append(data)
    return jsonify({'message': user_list}), 200


@app_look.route('/update_book_detail', methods=['POST'])
def remove_from_catalog():
    """Removes book from catalog if borrowed"""
    data = request.get_json()
    print(f"Received data: {data}")
    kwargs = {
        'id': data.get('id'),
        'available': data.get('available'),
        'due_date': data.get('due_date'),
        'user_id': data.get('user_id')
    }
    print(kwargs['user_id'], kwargs['due_date'], kwargs['available'])
    if not kwargs['id'] or kwargs['available'] is None or not kwargs['due_date'] or not kwargs['user_id']:
        return jsonify({'error': 'Missing required fields'}), 401
    book = storage.get_book_by_id(kwargs['id'])
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    book.available = kwargs['available']
    book.due_date = kwargs['due_date']
    book.user_id = kwargs['user_id']
    storage.save()

    book_dict = {
        'id': book.id,
        'title': book.title,
        'publisher': book.publisher,
        'category': book.category,
        'available': book.available,
        'due_date': book.due_date,
    }
    print(book_dict)
    return jsonify({'book removed': book_dict}), 201

@app_look.route('/users_borrowed_books', methods=['GET'])
def get_users_borrowed_books():
    """Return all users with books not in catalogue"""
    users = storage.get_users()
    print(users)
    if not users:
        return jsonify({'error': 'No users with books checked out'}), 404
    
    result = []
    for user in users:
        user_data = {
            'id': user.id,
            'email': user.email,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'books': user.books
        }
        result.append(user_data)
    return jsonify({'users': result}), 200

@app_look.route('/unavailable_books', methods=['GET'])
def get_unavailable_books():
    """Return all books that are not available"""
    try:
        books = storage.get_books()
        if not books:
            return jsonify({'error': 'No books in the catalogue'}), 404

        unavailable_books = []
        for book in books:
            if not book.available:
                data = {
                    'category': book.category,
                    'id': book.id,
                    'publisher': book.publisher,
                    'title': book.title,
                }
                unavailable_books.append(data)
            if not unavailable_books:
                return jsonify({'message': 'All books are available'}), 200
        return jsonify({'unavailable books': unavailable_books}), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred {e}'}), 500
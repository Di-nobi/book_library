from flask import jsonify, request, redirect, abort
import requests
from api.v1.views import app_look
from database import storage


@app_look.route('/add_book', methods=['POST'])
def add_book():
    """Adds new books to the catalogue"""
    kwargs = {
        'title': request.form.get('title'),
        'publisher': request.form.get('publisher'),
        'category': request.form.get('category'),
        'available': True
    }
    if not kwargs['title'] or not kwargs['publisher'] or not kwargs['category']:
        return jsonify({'error': 'Missing required fields'}), 400
    book = storage.add_books(**kwargs)

    url = 'http://localhost:5001/api/v1/update_catalog'
    try:
        requests.post(url, json={
            'title': book.title,
            'publisher': book.publisher,
            'category': book.category
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
    url = 'http://localhost:5001/remove_catalog'
    try:
        requests.delete(url, json={'book_id': book_id})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Could not notify the frontend {e}'}), 500
    return jsonify({'book removed': book}), 200

@app_look.route('/get_users', methods=['GET'])
def get_users():
    """Retrieves all users in the library"""
    users = storage.get_users()
    user_list = []
    for user in users:
        data = {
            user.firstName,
            user.lastName,
            user.email
        }
        user_list.append(data)
    return jsonify({'message': user_list}), 200

@app_look.route('/book_borrowed_user', methods=['GET'])
def get_users_with_books():
    """Return all users with books checked out"""
    users = storage.get_users_with_books()
    if not users:
        return jsonify({'error': 'No users with books checked out'}), 404
    
    result = []
    for user in users:
        user_data = {
            'id': user.id,
            'email': user.email,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'books': user.book
        }
        result.append(user_data)
    return jsonify({'users': result}), 200
@app_look.route('/unavailable_books', methods=['GET'])
def get_unavailable_books():
    """Return all books that are not available"""
    books = storage.get_books()
    if not books:
        return jsonify({'error': 'No books in the catalogue'}), 404

    unavailable_books = []
    for book in books:
        if not book.available:
            data = {
                'id': book.id,
                'title': book.title,
                'publisher': book.publisher,
                'category': book.category,
                'due_date': book.due_date
            }
            unavailable_books.append(data)
    return jsonify({'unavailable books': unavailable_books}), 200

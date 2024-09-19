from flask import jsonify, request, redirect, abort
from frontend.api.v1.views import app_look
from frontend.database import storage
from datetime import datetime, timedelta
import requests

@app_look.route('/update_catalog', methods=['POST'])
def add_book():
    """Adds new books to the catalogue"""
    data = request.get_json()
    print(f'Data found: {data}')
    kwargs = {
        'id': data.get('id'),
        'title': data.get('title'),
        'publisher': data.get('publisher'),
        'category': data.get('category'),

    }

    if not kwargs['title'] or not kwargs['publisher'] or not kwargs['category'] or not kwargs['id']:
        return jsonify({'error': 'Missing required fields'}), 401

    book = storage.add_books(**kwargs)
    book_list = {
        'id': book.id,
        'title': book.title,
        'publisher': book.publisher,
        'category': book.category,
    }
    print(book_list)
    return jsonify({'book updated': book_list }), 201

@app_look.route('/available_books', methods=['GET'])
def get_books():
    """Retrieves all books in the catalogue"""
    books = storage.get_books()
    book_list = []
    print(books)
    for book in books:
        if book.available:
            data = {
                'id': book.id,
                'title': book.title,
                'publisher': book.publisher,
                'category': book.category
            }
        book_list.append(data)
    return jsonify({'books': book_list}), 200

@app_look.route('/book/<book_id>', methods=['GET'])
def get_book(book_id):
    """Gets a book id"""
    a_book = storage.get_book_by_id(book_id)
    if not a_book:
        return jsonify({'error': 'Book not in catalogue'}), 404
    book = {
        'title': a_book.title,
        'publisher': a_book.publisher,
        'category': a_book.category
    }
    return jsonify({'book': book}), 200

@app_look.route('/book/<publisher>', methods=['GET'])
def get_publisher(publisher):
    """Gets a book by publisher"""
    book_by_publisher = storage.get_publisher(publisher)
    if not book_by_publisher:
        return jsonify({'error': 'Publisher not in catalogue'}), 404
    pub_book = {
        'title': book_by_publisher.title,
        'publisher': book_by_publisher.publisher,
        'category': book_by_publisher.category
    }
    return jsonify({'publisher_book': pub_book}), 201
    
@app_look.route('/book/<category>', methods=['GET'])
def get_category(category):
    """Gets a book by category"""
    book_by_category = storage.get_category(category)
    if not book_by_category:
        return jsonify({'error': 'Category of book does not exist'}), 404
    
    cat_book = {
        'title': book_by_category.title,
        'publisher': book_by_category.publisher,
        'category': book_by_category.category
    }
    return jsonify({'book_category': cat_book}), 201

@app_look.route('/borrow_book/<book_id>/<user_id>', methods=['POST'])
def borrow_book(book_id, user_id):
    """Borrows a particular book"""
    get_user = storage.get_users_by_id(user_id)
    if not get_user:
        return jsonify({'error': 'User not found'}), 404
    get_book = storage.get_book_by_id(book_id)
    if not get_book:
        return jsonify({'error': 'Book not found'}), 404
    if not get_book.available:
        return jsonify({'error': 'Book is already borrowed'})
    get_book.available = False
    get_book.due_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    get_book.user_id = user_id
    print(get_book.user_id)
    storage.save()
    url = 'http://localhost:5000/api/v1/update_book_detail'
    try:
        requests.post(url, json={
            'id': get_book.id,
            'available': get_book.available,
            'due_date': get_book.due_date,
            'user_id': get_book.user_id,
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Could not notify the backend {e}'}), 500
    return jsonify({'book borrowed': get_book.id}), 201

@app_look.route('/remove_catalog', methods=['DELETE'])
def remove_book():
    """Removes a book from the catalogue"""
    data = request.get_json()
    book = storage.get_book_by_id(data.get('id'))
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    storage.delete(book)
    storage.save()
    return jsonify({'book removed': book}), 200
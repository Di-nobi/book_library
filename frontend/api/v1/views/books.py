from flask import jsonify, request, redirect, abort
from frontend.api.v1.views import app_look
from frontend.database import storage



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
                'title': book.title,
                'publisher': book.publisher,
                'category': book.category
            }
        book_list.append(data)
    return jsonify({'books': book_list}), 200
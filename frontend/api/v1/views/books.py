from flask import jsonify, request, redirect, abort
from api.v1.views import app_look
from database import storage



@app_look.route('/update_catalog', methods=['POST'])
def add_book():
    """Adds new books to the catalogue"""
    data = request.get_json()

    kwargs = {
        'title': data.get('title'),
        'publisher': data.get('publisher'),
        'category': data.get('category'),
    }

    if not kwargs['title'] or not kwargs['publisher'] or not kwargs['category']:
        return jsonify({'error': 'Missing required fields'}), 401

    book = storage.add_books(**kwargs)
    book_list = {
        'title': book.title,
        'publisher': book.publisher,
        'category': book.category
    }
    return jsonify({'book updated': book_list }), 201
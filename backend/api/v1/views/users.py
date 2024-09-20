from flask import jsonify, request, redirect, abort
import requests
from api.v1.views import app_look
from database import storage

@app_look.route('/enroll_user', methods=['POST'])
def add_user():
    """Adds new users to the library"""
    
    data = request.get_json()
    print(f'Received data: {data}')
    kwargs = {
        'firstName': data.get('firstName'),
        'lastName': data.get('lastName'),
        'email': data.get('email'),
    }

    if not kwargs['firstName'] or not kwargs['lastName'] or not kwargs['email']:
        return jsonify({'error': 'Missing required fields'}), 401

    user = storage.add_users(**kwargs)
    user_list = {
        'firstName': user.firstName,
        'lastName': user.lastName,
        'email': user.email
    }
    print(user_list)
    return jsonify({'user added': user_list }), 201
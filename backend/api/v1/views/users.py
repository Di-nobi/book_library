from flask import jsonify, request, redirect, abort
import requests
from backend.api.v1.views import app_look
from backend.database import storage

@app_look.route('/enroll_user', methods=['POST'])
def add_user():
    """Adds new users to the library"""
    
    data = request.get_json()

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
    return jsonify({'user added': user_list }), 201
from flask import jsonify, request, redirect, abort
from api.v1.views import app_look
from database import storage
import requests

@app_look.route('/enroll_user', methods=['POST'])
def enroll_user():
    """Adds new users to the library"""
    kwargs = {
        'firstName': request.form.get('firstName'),
        'lastName': request.form.get('lastName'),
        'email': request.form.get('email'),
    }
    if not kwargs['firstName'] or not kwargs['lastName'] or not kwargs['email']:
        return jsonify({'error': 'Missing required fields'}), 400
    user = storage.add_users(**kwargs)

    url = 'http://localhost:5000/api/v1/enroll_user'
    try:
        requests.post(url, json={
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Could not notify the frontend {e}'}), 500
    
    user_data = {
        'id': user.id,
        'firstName': user.firstName,
        'lastName': user.lastName,
        'email': user.email
    }
    return jsonify({'user added': user_data }), 201
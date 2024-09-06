from flask import Blueprint, request, jsonify
from extensions import mongo, bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print("Received registration data:", data)  # Debugging log
        user = mongo.db.users.find_one({'username': data['username']})
        
        if user:
            return jsonify({'message': 'User already exists'}), 409

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        mongo.db.users.insert_one({
            'username': data['username'],
            'email': data['email'],
            'password': hashed_password
        })

        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        print(f"Error during registration: {e}")  # Debugging log
        return jsonify({'message': 'Server error occurred'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print("Received login data:", data)  # Debugging log
        user = mongo.db.users.find_one({'username': data['username']})

        if user and bcrypt.check_password_hash(user['password'], data['password']):
            access_token = create_access_token(identity=str(user['_id']))
            return jsonify(access_token=access_token), 200

        return jsonify({'message': 'Invalid credentials'}), 401

    except Exception as e:
        print(f"Error during login: {e}")  # Debugging log
        return jsonify({'message': 'Server error occurred'}), 500
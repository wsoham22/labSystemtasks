import os
import jwt
import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Blueprint, jsonify, request, g
from bson import json_util

user_bp = Blueprint('user_bp', __name__, url_prefix='/labSystem/v1/users')

# Token Validation Middleware
def token_required(f):
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        print("Received Token:", token)  # Add this line for debugging

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            data = jwt.decode(token.split(' ')[1], os.getenv("SECRET_KEY"), algorithms=["HS256"])
            g.user = data  # Store the decoded token data in Flask's g object for later use
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated_function

class UserModel:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client['LabSystemsDatabase']
        self.collection = self.db['user']

    def find_all_users(self):
        users = self.collection.find()
        user_list = []
        for user in users:
            user['_id'] = str(user['_id'])
            user_list.append(user)
        return user_list

    def find_user_by_id(self, user_id):
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        return json_util.dumps(user) if user else None

    def create_user(self, name, email, password, address, country, state, interests, role='user'):  # Default role set to 'user'
        user_data = {
            "name": name,
            "password": password,
            "email": email,
            "address": address,
            "country": country,
            "state": state,
            "interests": interests,
            "role": role
        }
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)

    def delete_user(self, user_id):
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count

    def find_user_by_email_and_password(self, email, password):
        return self.collection.find_one({"email": email, "password": password})

@user_bp.route('/', methods=['GET'])
def get_all_users():
    user_model = UserModel()
    users = user_model.find_all_users()
    return jsonify(users)

@user_bp.route('/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user_model = UserModel()
    user = user_model.find_user_by_id(user_id)
    if user:
        return user
    else:
        return jsonify({"error": "User not found"}), 404

@user_bp.route('/create', methods=['POST'])
def create_user():
    new_user_data = request.json
    user_model = UserModel()
    user_id = user_model.create_user(**new_user_data)
    return jsonify({"message": "User created successfully", "user_id": user_id}), 201

# Protected delete route
# @user_bp.route('/<user_id>', methods=['DELETE'])
# @token_required
# def delete_user(user_id):
#     user_model = UserModel()
#     deleted_count = user_model.delete_user(user_id)
#     if deleted_count:
#         return jsonify({'User data deleted Successfully!'}), 204
#     else:
#         return jsonify({"error": "User not found"}), 404

@user_bp.route('/<user_id>', methods=['PATCH'])
def update_user(user_id):
    user_model = UserModel()
    update_data = request.json
    updated_count = user_model.collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    if updated_count.modified_count:
        return jsonify({"message": "User data updated successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        auth_data = request.json
        email = auth_data.get('email')
        password = auth_data.get('password')

        user_model = UserModel()
        user = user_model.find_user_by_email_and_password(email, password)

        if not user:
            return jsonify({"error": "Invalid email or password"}), 401

        # Generate JWT token with expiration time
        token = jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           os.getenv("SECRET_KEY"))
        return jsonify({"token": token}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred while processing your request"}), 500
@user_bp.route('/<user_id>', methods=['DELETE'],endpoint= 'deleteuser')
@token_required
def delete_user(user_id):
    user_model = UserModel()
    deleted_count = user_model.delete_user(user_id)
    if deleted_count:
        return jsonify({'message': 'User data deleted successfully'}), 204
    else:
        return jsonify({"error": "User not found"}), 404

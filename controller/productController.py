import os
import jwt
from bson import json_util
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Blueprint, jsonify, request
from .userController import token_required

product_bp = Blueprint('product_bp', __name__, url_prefix='/labSystem/v1/products')

class ProductModel:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client['LabSystemsDatabase']
        self.collection = self.db['products']

    def find_all_products(self):
        products = self.collection.find()
        return [product for product in products]

    def find_product_by_id(self, product_id):
        product = self.collection.find_one({"_id": ObjectId(product_id)})
        return json_util.dumps(product) if product else None

    def delete_product(self, product_id):
        result = self.collection.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count
    def create_product(self, product_data):
        result = self.collection.insert_one(product_data)
        return str(result.inserted_id)

product_model = ProductModel()

@product_bp.route('/', methods=['GET'], endpoint='get_all_products')
@token_required
def get_all_products():
    products = product_model.find_all_products()
    return jsonify(products)


@product_bp.route('/create', methods=['POST'], endpoint='create-new-product')
@token_required
def create_product():
    product_data = request.json
    product_id = product_model.create_product(product_data)
    return jsonify({"message": "Product created successfully", "product_id": product_id}), 201

@product_bp.route('/<product_id>', methods=['DELETE'], endpoint='delete-product')
@token_required
def delete_product(product_id):
    deleted_count = product_model.delete_product(product_id)
    if deleted_count:
        return '', 204  # Return empty response with 204 status code
    else:
        return jsonify({"error": "Product not found"}), 404

@product_bp.route('/<product_id>', methods=['PATCH'], endpoint='editproducts')
@token_required
def update_product(product_id):
    update_data = request.json
    updated_count = product_model.collection.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
    if updated_count.modified_count:
        return jsonify({"message": "Product data updated successfully"}), 200
    else:
        return jsonify({"error": "Product not found"}), 404
@product_bp.route('/<product_id>', methods=['GET'], endpoint='get-a-product')
@token_required
def get_product(product_id):
    try:
        product = product_model.find_product_by_id(product_id)
        if product:
            return jsonify(product)
        else:
            error_message = "Product not found for ID: {}".format(product_id)
            return jsonify({"error": error_message}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred while processing your request"}), 500






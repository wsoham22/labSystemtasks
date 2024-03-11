# # productModel.py
# from pymongo import MongoClient
# from bson.objectid import ObjectId
#
#
# class UserModel:
#     def __init__(self, db_name='LabSystemsDatabase'):
#         self.client = MongoClient('mongodb://localhost:27017/')
#         self.db = self.client[db_name]
#         self.collection = self.db['product']
#
#     def create_product(self, name, image, genre, cost, description):
#         product_data = {
#             "name": name,
#             "image": image,
#             "genre": genre,
#             "cost": cost,
#             "description": description,
#             "saved": False,
#             "add_to_cart": False
#         }
#         result = self.collection.insert_one(product_data)
#         return str(result.inserted_id)
#
#     def get_product(self, product_id):
#         return self.collection.find_one({"_id": ObjectId(product_id)})
#
#     def update_product(self, product_id, update_data):
#         result = self.collection.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
#         return result.modified_count
#
#     def delete_product(self, product_id):
#         result = self.collection.delete_one({"_id": ObjectId(product_id)})
#         return result.deleted_count
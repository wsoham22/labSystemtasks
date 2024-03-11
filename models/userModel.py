#
# from pymongo import MongoClient
# from bson.objectid import ObjectId
#
# class UserModel:
#     def __init__(self, db_name='LabSystemsDatabase'):
#         self.client = MongoClient('mongodb://localhost:27017/')
#         self.db = self.client[db_name]
#         self.collection = self.db['users']
#
#     def create_user(self, name,password,email, address, country, state, interests):
#         user_data = {
#             "name": name,
#             "password": password,
#             "email": email,
#             "address": address,
#             "country": country,
#             "state": state,
#             "interests": interests
#         }
#         result = self.collection.insert_one(user_data)
#         return str(result.inserted_id)
#
#     def find_user_by_email_and_password(self, email, password):
#         return self.collection.find_one({"email": email, "password": password})
#
#     def get_user(self, user_id):
#         return self.collection.find_one({"_id": ObjectId(user_id)})
#
#     def find_user_by_email(self, email):
#         return self.collection.find_one({"email": email})

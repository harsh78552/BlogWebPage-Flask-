from pymongo import MongoClient
import re
from email_validator import validate_email
import hashlib


class UserDatabase:
	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017/')
		self.db = self.client['Blog']
		self.collection = self.db['data']

	def insert_user(self, user_name, user_contact, user_mail, user_password, role='user'):
		try:
			validate_email(user_mail, check_deliverability=False)
			valid_email = True
		except Exception as error:
			valid_email = False
		if valid_email:
			pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{8,}$'
			if bool(re.match(pattern, user_password)):
				hash_password = hashlib.sha256(user_password.encode('utf-8')).hexdigest()
				insert_data = {"user_name": user_name.lower(), "user_contact": user_contact, "user_mail": user_mail,
				               "user_password": hash_password, 'role': role}
				self.collection.insert_one(insert_data)
				return {"message": "User added successfully...."}
			return (
				"password at least 8 characters\n. One uppercase\n. at least one special symbol\n. a lowercase letter\n. a digit")
		else:
			return {"error": 'not a valid email'}

	def get_user_from_name(self, name, email):
		get_data = self.collection.find_one({"user_name": name.lower(), "user_mail": email})
		if get_data:
			user_data_dict = {
				"_id": str(get_data.get("_id")),
				"user_name": get_data.get('user_name'),
				"user_contact": get_data.get('user_contact'),
				"user_mail": get_data.get('user_mail'),
				"user_password": get_data.get('user_password'),
				"role": get_data.get("role"),
			}
			return [user_data_dict]
		else:
			return None

	def get_all_user_data(self):
		user_list = []
		get_data = self.collection.find()
		for data in get_data:
			user_data_dict = {
				"_id": str(data.get("_id")),
				"user_name": data.get("user_name"),
				"user_contact": data.get("user_contact"),
				"user_mail": data.get("user_mail"),
				"user_password": data.get("user_password"),
				"role": data.get("role"),
			}
			user_list.append(user_data_dict)
		return user_list

	# return user_list

	def delete_user(self, name, password):
		get_data = self.collection.find_one({"user_name": name.lower(), "user_password": password})
		if get_data:
			self.collection.delete_one(get_data)
			return {"message": "delete successful"}
		else:
			return {'message': "user not exist..."}

# def update_user_data(self, name, email, password):
# 	get_data = self.collection.find_one({"user_name": name.lower(), "user_password": password})
# 	if get_data:
# 		if name and password:
# 			self.collection.updateOne({"user_name": name}, {$set: {"user_password": password}})


# db = UserDatabase()
# db.insert_user("Adarsh Tiwari", "8235269156", "adarsh082352@gmail.com", "Adarsh@123")
# db.insert_user("Harsh Tiwari", "7654092577", "harsh844509@gmail.com", "Harsh@123",role='admin')
# db.get_user_from_name("Adarsh Tiwari", "at6031751@gmail.com")
# db.get_all_user_data()
# db.update_user_data("Harsh Tiwari", "harsh844509@gmail.com", "jiohiwug5")
# db.delete_user("Adarsh Tiwari", "Adarsh@123")

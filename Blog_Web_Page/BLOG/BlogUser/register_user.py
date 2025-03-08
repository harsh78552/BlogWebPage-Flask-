from flask import request, json, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from Blog_Web_Page.Database.USER.user import UserDatabase
from Blog_Web_Page.SCHEMA.user_schema import UserRegisterSchema

blp = Blueprint("register", __name__, description="user register")


@blp.route('/user--register')
class RegisterUser(MethodView):
	def __init__(self):
		self.user_db = UserDatabase()

	@blp.arguments(UserRegisterSchema)
	def post(self, request_data):
		user_name = request_data['user_name']
		user_contact = request_data['user_contact']
		user_mail = request_data['user_mail']
		password = request_data['user_password']
		user_exist = self.user_db.get_user_from_name(user_name, user_mail)
		if user_exist is None:
			self.user_db.insert_user(user_name, user_contact, user_mail, password)
			return jsonify({"message": "user registered successfully..."}), 200
		return {"message": "user already registered...."}

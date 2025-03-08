from flask import jsonify, request
from flask_smorest import Blueprint
from flask.views import MethodView
from Blog_Web_Page.Database.USER.user import UserDatabase
import hashlib
from flask_jwt_extended import create_access_token, set_access_cookies
from datetime import timedelta

blp = Blueprint("login-user", __name__, description="user login")


@blp.route("/user-login")
class UserLogin(MethodView):
	def __init__(self):
		self.user_db = UserDatabase()

	def post(self):
		user_data = request.get_json()
		user_name = user_data.get('user_name')
		user_email = user_data.get('user_mail')
		password = user_data.get('user_password')
		hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
		user_data_ = self.user_db.get_user_from_name(user_name, user_email)
		if user_data_ and user_data_[0]['role'] == "user":
			if user_data_[0]['user_name'] == user_name.lower() and user_data_[0]['user_mail'] == user_email and \
					user_data_[0][
						'user_password'] == hash_password:
				access_token = create_access_token(identity=user_data_[0]["_id"],
				                                   additional_claims={"_id": str(user_data_[0]["_id"]),
				                                                      "user_name": user_data_[0]["user_name"],
				                                                      "user_email": user_data_[0]["user_mail"],
				                                                      "role": user_data_[0]['role']},
				                                   expires_delta=timedelta(hours=48))
				response = jsonify({"message": ' user login successfully'})
				set_access_cookies(response, access_token)
				return response, 200
			return jsonify({"message": "Invalid credentials..."}), 401
		return jsonify({'message': 'user not exist...'}), 404

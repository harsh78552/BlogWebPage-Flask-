from flask import request, jsonify
from Blog_Web_Page.Database.USER.user import UserDatabase
from flask_smorest import Blueprint
from flask.views import MethodView
import hashlib
from flask_jwt_extended import create_access_token, set_access_cookies
from datetime import timedelta

blp = Blueprint("login-admin", __name__, description="superuser login")


@blp.route("/super-user-login")
class SuperUserLogin(MethodView):
	def __init__(self):
		self.user_db = UserDatabase()

	def post(self):
		super_user_data = request.get_json()
		super_user_name = super_user_data.get("user_name")
		super_user_mail = super_user_data.get("user_mail")
		hash_password = hashlib.sha256(super_user_data.get("user_password").encode('utf-8')).hexdigest()
		super_user_get = self.user_db.get_user_from_name(super_user_name, super_user_mail)
		if super_user_get and super_user_get[0]['role'] == 'admin':
			if super_user_get[0]['user_name'] == super_user_name.lower() and super_user_get[0][
				'user_mail'] == super_user_mail and \
					super_user_get[0]['user_password'] == hash_password:
				access_token = create_access_token(identity=super_user_get[0]['_id'],
				                                   additional_claims={"_id": str(super_user_get[0]['_id'])},
				                                   expires_delta=timedelta(hours=1))

				response = jsonify({"message": ' admin login successfully'})
				set_access_cookies(response, access_token)
				return response, 200
			return jsonify({'message': "invalid credentials..."}), 401
		return jsonify({'message': 'user not exist...'}), 404

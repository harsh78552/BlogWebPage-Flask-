from flask import jsonify, request
from flask_smorest import Blueprint
from flask.views import MethodView
from Blog_Web_Page.BLOG.Blog_SuperUser.super_user_bloclkist import BLOCKLIST_
from flask_jwt_extended import jwt_required, get_jwt, unset_jwt_cookies

blp = Blueprint("super_user-logout", __name__, description="super-user logout")


@blp.route("/super-user-logout")
class SuperUserLogout(MethodView):
	@jwt_required()
	def post(self):
		jti = get_jwt()['jti']
		BLOCKLIST_.add(jti)
		response = jsonify({"message": "logged out successfully."})
		unset_jwt_cookies(response)
		return response, 200



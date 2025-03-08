from flask import jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from Blog_Web_Page.BLOG.BlogUser.user_blocklist import BLOCKLIST
from flask_jwt_extended import jwt_required, get_jwt, unset_jwt_cookies

blp = Blueprint("logout", __name__, description="user logout")


@blp.route("/user-logout")
class UserLogout(MethodView):
	@jwt_required()
	def post(self):
		jti = get_jwt()['jti']
		role = get_jwt().get("role")
		BLOCKLIST.add(jti)
		response = jsonify({"message": f"{role.capitalize()} logged out successfully."})
		unset_jwt_cookies(response)
		return response, 200

from flask import Flask
from flask_smorest import Api
from Blog_Web_Page.BLOG.Blog_SuperUser.super_user_login import blp as SuperUserLoginBlueprint
from Blog_Web_Page.BLOG.Blog_SuperUser.super_user_logout import blp as SuperUserLogoutBlueprint
from Blog_Web_Page.BLOG.BlogUser.user_login import blp as UserLoginBlueprint
from Blog_Web_Page.BLOG.Blog_SuperUser.blog_post import blp as BlogPostBlueprint
from Blog_Web_Page.BLOG.Blog_SuperUser.user_RUD_operation import blp as UserRUDBlueprint
from Blog_Web_Page.BLOG.BlogUser.contact import blp as ContactBluePrint
from Blog_Web_Page.BLOG.Blog_SuperUser.super_user_bloclkist import BLOCKLIST_
from Blog_Web_Page.BLOG.BlogUser.user_logout import blp as UserLogout
from flask_jwt_extended import JWTManager, unset_jwt_cookies
import cloudinary.api
from flask_mail import Mail
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=["http://localhost:63342", "http://localhost:63348"], supports_credentials=True)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['API_TITLE'] = 'blog web_page api'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = "/"
app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui"
app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config['JWT_SECRET_KEY'] = "gutwulh34cfn2u734809(*^^^*&*(E*#)*_#)&"

app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config["JWT_COOKIE_SAMESITE"] = 'None'
app.config['JWT_COOKIE_HTTPONLY'] = True

cloudinary.config(
	cloud_name="dofbbfgg4",
	api_key="596269484844184",
	api_secret="0uzI8tt4-bGFwAZuTfOiEMEQD2o",
	secure=True
)

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "ht728350@gmail.com"
app.config['MAIL_PASSWORD'] = "hnzx xeiq sqcj vglh"
api = Api(app)
jwt = JWTManager(app)
mail_ = Mail(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jte_header, jwt_payload):
	return jwt_payload['jti'] in BLOCKLIST_


@jwt.revoked_token_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
	return (
		{"description": "User has been logged out....",
		 'error': 'token_revoked'}
	), 401


@app.after_request
def unset_jwt(response):
	if response.status_code == 401:
		unset_jwt_cookies(response)
	return response


api.register_blueprint(SuperUserLoginBlueprint)
api.register_blueprint(SuperUserLogoutBlueprint)
api.register_blueprint(UserLoginBlueprint)
api.register_blueprint(BlogPostBlueprint)
api.register_blueprint(UserLogout)
api.register_blueprint(UserRUDBlueprint)
api.register_blueprint(ContactBluePrint)

if __name__ == "__main__":
	app.run(debug=True, port=5005)

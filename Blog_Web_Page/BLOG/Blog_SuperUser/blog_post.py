from bson import ObjectId
from flask import request, jsonify
from Blog_Web_Page.Database.BLOG_POST.BlogPost import BlogPostDatabase
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from datetime import datetime
import cloudinary.uploader

blp = Blueprint('blog-post', __name__, description="blog post by user....")
now_ = datetime.now()


@blp.route('/check-auth')
@jwt_required()
def check_auth():
	current_user = get_jwt_identity()
	return jsonify({"user": current_user}), 200


@blp.route('/add-post-in-existing-post')
class AddPostInExistingPost(MethodView):
	def __init__(self):
		self.post_db = BlogPostDatabase()

	@jwt_required()
	def post(self):
		print(request.headers)
		post_id = request.form.get('post_id')
		print(post_id)
		post_title = request.form.get('title')
		print(post_title)
		content = request.form.get('content')
		print(content)
		updated_at = now_
		self.post_db.update_existing_post(post_id, post_title, content, updated_at)
		return jsonify({"message": "Post added successfully...."}), 200


@blp.route('/admin-upload-post')
class UserPostBlog(MethodView):
	def __init__(self):
		self.blog_db = BlogPostDatabase()

	@jwt_required()
	def post(self):
		try:
			title = request.form.get("title")
			content = request.form.get("content")
			author_id = get_jwt_identity()
			created_at = now_
			updated_at = now_
			category = request.form.get("category")
			tags = request.form.get("tags")
			image_url = None
			image_file = request.files.get("image_file")
			if image_file:
				try:
					upload_result = cloudinary.uploader.upload(image_file)
					image_url = upload_result["secure_url"]
				except Exception as error:
					return {"error": str(error)}, 500
			response = self.blog_db.insert_blog_data(title, content, author_id, created_at, updated_at, category,
			                                         tags,
			                                         image_url)
			return response, 201
		except Exception as error:
			return {"error": str(error)}, 500

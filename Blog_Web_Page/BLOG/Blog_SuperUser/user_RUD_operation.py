from flask import request, jsonify
from Blog_Web_Page.Database.BLOG_POST.BlogPost import BlogPostDatabase
from Blog_Web_Page.Database.USER.user import UserDatabase
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

blp = Blueprint("Read-Update-Delete operation", __name__, description="user perform Read-Update-Delete-Operation")


@blp.route('/get-blog-post')
class BlogRead(MethodView):
	def __init__(self):
		self.blog_db = BlogPostDatabase()

	def get(self):
		title = request.args.get("title")
		print(title)
		if not title:
			return self.blog_db.get_all_post()
		else:
			blog_post_data = self.blog_db.get_one_post(title.upper())
			return blog_post_data


@blp.route('/get-blog-post-id')
class BlogRead(MethodView):
	def __init__(self):
		self.blog_db = BlogPostDatabase()

	def get(self):
		post_id = request.args.get("id")
		data = self.blog_db.get_one_post_id(post_id)
		return data


@blp.route("/extract-category")
class ExtractCategory(MethodView):
	def __init__(self):
		self.blog_db = BlogPostDatabase()

	def get(self):
		if request.args.get("") is None:
			data = self.blog_db.get_all_post()
			category_list = []
			for category_ in data:
				category_dict = {"category": category_['category'], "post": category_['BLOG_TITLE']}
				category_list.append(category_dict)
				print(category_list)
			return category_list


@blp.route('/update-blog')
class BlogUpdate(MethodView):
	def __init__(self):
		self.blog_db = BlogPostDatabase()

	@jwt_required()
	def put(self):
		data = request.get_json()
		id = data['id']
		content = data['content']
		post_data = self.blog_db.get_one_post_id(id)
		if id == post_data[0]['post_id']:
			self.blog_db.update_post(id, content)
			return {"message": "post-updated successfully..."}, 200
		return {"message": "post not updates successfully..."}, 400


@blp.route("/delete-post")
class AdminDelPost(MethodView):
	def __init__(self):
		self.post_db = BlogPostDatabase()

	@jwt_required()
	def delete(self):
		_id = request.get_json()
		post_id = _id['post_id']
		if self.post_db.delete_post(post_id):
			return jsonify({'message': "post deleted successfully..."}), 200
		return jsonify({"message": "some error occurred...."})

from bson import ObjectId
from pymongo import MongoClient


class BlogPostDatabase:
	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017/')
		self.db = self.client['BlogPost']
		self.collection = self.db['blog_data']

	def insert_blog_data(self, title, content, author_id, created_at, updated_at, category, tags, post_image_url):
		insert_data = {"BLOG_TITLE": [title.upper()], "content": [{"title": title.upper(), "text": content}],
		               "author_id": author_id,
		               "created_at": created_at,
		               "updated_at": updated_at, "category": category.upper(), "tags": [tags],
		               "image_url": post_image_url}
		self.collection.insert_one(insert_data)
		get_one_post = self.collection.find_one({"BLOG_TITLE": title.upper()})
		post_id = str(get_one_post.get("_id"))
		return {"message": "Post added successfully....", 'post_id': post_id}

	def get_all_post(self):
		get_all_post = self.collection.find()
		if get_all_post:
			post_list = []
			for post in get_all_post:
				post_dict = {"BLOG_TITLE": post.get("BLOG_TITLE"),
				             "content": post.get("content"),
				             "author_id": post.get("author_id"),
				             "category": post.get("category"),
				             "post_id": str(post.get("_id")),
				             "tags": post.get("tags"),
				             'image_url': post.get("image_url")
				             }
				post_list.append(post_dict)
			return post_list
		else:
			return {"message": "no any content..."}

	def get_one_post(self, title):
		get_data = self.collection.find_one({"BLOG_TITLE": title})
		list_ = get_data['content']
		for data in list_:
			if data['title'] == title:
				blog_post_dict = {"post_id": str(get_data.get("_id")), "BLOG_TITLE": data['title'],
				                  "blog-post": data['text']}
				return [blog_post_dict]

	def get_one_post_id(self, post_id_):
		get_data = self.collection.find_one({str("_id"): ObjectId(post_id_)})
		if get_data:
			post_dict = {"post_id": str(get_data.get("_id")),
			             "BLOG_TITLE": get_data.get("BLOG_TITLE"),
			             "content": get_data.get("content"),
			             "category": get_data.get("category"),
			             "tags": get_data.get("tags"),
			             'image_url': get_data.get("image_url")}
			return [post_dict]
		else:
			return {"message": "post-id not matched from this  blog-post..."}

	def update_post(self, id, content):
		get_data = self.collection.update_one(
			{'_id': ObjectId(id)},
			{"$set": {"content": content}}
		)
		return {"message": "blog update successfully....."}

	def update_existing_post(self, post_id, new_title, new_content, update_at):
		try:
			get_data = self.collection.update_one({"_id": ObjectId(post_id)}, {
				"$push": {"BLOG_TITLE": new_title.upper(),
				          "content": {"title": new_title.upper(), "text": new_content}},
				"$set": {"updated_at": update_at}})
			return {"message": "Blog updated successfully!"}
		except Exception as error:
			return str(error)

	def delete_post(self, post_id):
		del_post = self.collection.delete_one({"_id": ObjectId(post_id)})
		if del_post.deleted_count > 0:
			return True
		else:
			return False

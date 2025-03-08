from marshmallow import fields, Schema


class BlogPostSchema(Schema):
	blog_id = fields.Str(required=True)
	BLOG_TITLE = fields.Str(required=True)
	content = fields.List(fields.Str(), required=True, missing=[])
	author_id = fields.Str(required=True)
	created_at = fields.DateTime(required=True)
	updated_at = fields.DateTime(required=True)
	category = fields.Str(required=True)
	tags = fields.List(fields.Str(), required=True, missing=[])

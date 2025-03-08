from marshmallow import fields, Schema


class UserRegisterSchema(Schema):
	user_name = fields.Str(required=True)
	user_contact = fields.Str(required=True)
	user_mail = fields.Str(required=True)
	user_password = fields.Str(required=True)
	

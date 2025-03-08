from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_mail import Message

blp = Blueprint("message", __name__, description="user send message....")


@blp.route("/user-send-message")
class SendMessage(MethodView):
	@staticmethod
	def post():
		from Blog_Web_Page.app import mail_
		mail_data = request.get_json()
		user_mail = mail_data['user_mail']
		user_message = mail_data['message']
		try:
			subject = "regarding your time..."
			msg = Message(subject=subject, sender=user_mail, recipients=["ht728350@gmail.com"], reply_to=user_mail)
			msg.body = f"From:<{user_mail}>\n\nMessage:\n{user_message}"
			mail_.send(msg)
			return {"message": "mail sent successfully...."}
		except Exception as e:
			return str(e)

import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from main import  mail
from flask import current_app



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/profilePics", picture_fn)

    #resize picture
    outputSize = (125,125)
    new = Image.open(form_picture)
    new.thumbnail(outputSize)

    new.save(picture_path)
    return picture_fn

# MAIL SENDER
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Requset", sender="flaskblogsender@gmail.com", recipients=[user.email])
    msg.body = f"""
To reset your password, visit the following link {url_for('users.reset_token', token=token, _external= True)}
If you did not make this request then simply ignore this email and no changes will be made.
"""
    mail.send(msg)


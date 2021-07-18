from main.users.utils import save_picture, send_reset_email
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, login_user, current_user, logout_user
from main import db, bcrypt
from main.models import User, Post
from main.users.forms import ResetPasswordForm, LoginForm, UpdateAccountForm, RequestResetform, RegistrationForm
from main.users.utils import save_picture, send_reset_email


users = Blueprint("users", __name__)

@users.route("/register", methods=["POST","GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("base.home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data, email=form.email.data, password= hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f"Your Account has been Created.", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("base.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("base.home"))
        else:
            flash(f"Please Check Your Email And Password", "danger")
    return render_template("login.html", title="Login", form=form)

@users.route("/logout", methods=["POST","GET"])
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/account", methods=["POST","GET"])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.mail = form.email.data
        db.session.commit()
        flash("Your account has been updated", "success")
        return redirect(url_for("users.account"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profilePics/' + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)



@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page",1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=2)
    return render_template("user_posts.html", posts=posts, user=user)

@users.route("/reset_password", methods=["POST","GET"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("base.home"))
    form = RequestResetform()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title= "Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["POST","GET"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("base.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated.", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title= "Reset Password", form=form)
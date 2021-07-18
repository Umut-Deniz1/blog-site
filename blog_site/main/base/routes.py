from flask import Blueprint, render_template, request
from main.models import Post




base = Blueprint("base", __name__)

@base.route("/")
@base.route("/home")
def home():
    page = request.args.get("page",1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template("index.html", posts=posts)

@base.route("/about")
def about():
    return render_template("about.html")
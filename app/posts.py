from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models.Post import Post
from .forms import PostForm
from dotenv import load_dotenv
from . import db
import os

project_folder = os.path.expanduser("")
load_dotenv(os.path.join(project_folder, ".env"))

posts = Blueprint("posts", __name__)

@posts.route("/my-posts", methods=["GET"])
@login_required
def index():
    return render_template("posts/index.html", posts=current_user.posts)

@posts.route("/posts/<id>", methods=["GET"])
@login_required
def details(id):
    post = Post.query.filter_by(id=id).first()
    return render_template("posts/details.html", post=post)


@posts.route("/posts/create/<book_id>", methods=["GET", "POST"])
@login_required
def create(book_id):
    form = PostForm()
    if request.method == "POST" and form.validate_on_submit():
        title = request.form.get("title")
        content = request.form.get("content")
        post = Post(title, content, current_user.id, book_id)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for("posts.index"))
        
    return render_template("posts/create.html", form=form)
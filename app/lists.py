from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models.Book import Book, Author, Category
from .models.List import List
from .forms import ListForm
from dotenv import load_dotenv
from . import db
import os

project_folder = os.path.expanduser("")
load_dotenv(os.path.join(project_folder, ".env"))

lists = Blueprint("lists", __name__)

@lists.route("/my-lists", methods=["GET"])
@login_required
def index():
    return render_template("lists/index.html", lists=current_user.lists)

@lists.route("/list/<id>/books", methods=["GET"])
@login_required
def books(id):
    list = List.query.filter_by(id=id).first()
    print(list.books)
    return render_template("lists/books.html", list=list)


@lists.route("/list/create", methods=["GET", "POST"])
@login_required
def create():
    form = ListForm()
    if request.method == "POST" and form.validate_on_submit():
        name = request.form.get("name")
        list = List(name=name)
        current_user.lists.append(list)
        db.session.commit()
        return redirect(url_for("lists.index"))
        
    return render_template("lists/create.html", form=form)
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models.Book import Book, Author, Category
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
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models.Book import Book, Author, Category
from .forms import SearchBookForm, BookListForm
from .BookGoogleApi import BookGoogleApi
from dotenv import load_dotenv
from .models.List import List
from . import db
import os

project_folder = os.path.expanduser("")
load_dotenv(os.path.join(project_folder, ".env"))

books = Blueprint("books", __name__)

@books.route("/", methods=["GET", "POST"])
@login_required
def home():
    form = SearchBookForm()
    books_results = []

    if request.method == "POST" and form.validate_on_submit():
        search_str = form.search.data
        google_api_url = os.getenv("GOOGLE_API_URL")
        book_google_api = BookGoogleApi(google_api_url)
        books_results = book_google_api.get_results_books_api(search_str)
        if books_results["status"] == "error":
            flash("An error occured", category="error")

        books_results = books_results["books"]

    return render_template("books/home.html", form=form, books_results=books_results)


@books.route("/books/details/<id>", methods=["GET", "POST"])
@login_required
def details(id):
    book = Book.query.filter_by(id=id).first()
    book_list_form = BookListForm()

    book_list_form.lists.choices = [(c.id, c.name) for c in current_user.lists]
    preselected_list_ids = [list.id for list in book.lists]
    book_list_form.lists.default = preselected_list_ids
    book_list_form.process()

    if request.method == "POST":
        for list in  book_list_form.lists.data:
            list = List.query.filter_by(id=list).first()
            list.books.append(book)
            db.session.commit()
                        
    if not book:
        google_api_url = os.getenv("GOOGLE_API_URL")
        book_google_api = BookGoogleApi(google_api_url)
        result = book_google_api.get_result_book_details(id)

        if result["status"] == "error":
            flash("An error occured", category="error")
        else:
            book = result["book"]

    return render_template("books/details.html", book=book, book_list_form=book_list_form)


@books.route("/my-books", methods=["GET"])
@login_required
def favorites_books():
    user_books = current_user.books_list
    return render_template("books/favorites.html", books=user_books)


@books.route("/books/remove/<id>", methods=["GET"])
@login_required
def remove_favorites(id):
    book = Book.query.filter_by(id=id).first()
    current_user.books_list.remove(book)
    db.session.commit()
    return redirect(url_for("books.favorites_books"))


@books.route("/books/add/<id>", methods=["GET"])
@login_required
def add_favorite(id):
    google_api_url = os.getenv("GOOGLE_API_URL")
    book_google_api = BookGoogleApi(google_api_url)

    result = book_google_api.get_result_book_details(id)

    if result["status"] == "ok":
        book_data = result["book"]
        authors = []

        # check if the book is already in the db
        book = Book.query.filter_by(google_api_id=id).first()

        if not book:
            print(book_data)
            book = Book(
                title=book_data["title"],
                google_api_id=book_data["id"],
                image_url=book_data["image_url"],
                description=book_data["description"],
                published_date=book_data["published_date"],
            )

            db.session.add(book)
            # must check authors, categories and add them if needed
            for author_name in book_data["authors"]:
                author = Author.query.filter_by(name=author_name).first()
                print(author_name)
                print(author)

                if not author:
                    print("ok")
                    author = Author(name=author_name)
                    db.session.add(author)
                    book.authors.append(author)
                    db.session.commit()
                authors.append(author)

            # categories = []

            for category_name in book_data["categories"]:
                category = Category.query.filter_by(name=category_name).first()

                if not category:
                    category = Category(name=category_name)
                    db.session.add(category)
                    book.categories.append(category)

        current_user.books_list.append(book)

        db.session.commit()
        flash("OK")

    if result["status"] == "error":
        flash("An error occured", category="error")

    return redirect(url_for("books.favorites_books"))

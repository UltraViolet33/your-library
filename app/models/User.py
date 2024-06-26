from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import validates
from flask_login import UserMixin
from .. import db
import re
from .List import List
from .Post import Post


books_list_table = db.Table(
    "books_list",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("book_id", db.Integer, db.ForeignKey("books.id")),
)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    google_id = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password_hashed = db.Column(db.String(255))

    books_list = db.relationship(
        "Book", secondary=books_list_table, backref="users_books_list"
    )

    lists = db.relationship("List", backref="user", passive_deletes=True)
    posts = db.relationship("Post", backref="user", passive_deletes=True)

    def __init__(self, email, username, password_plaintext=None, google_id=None):
        self.email = email
        self.username = username
        self.google_id = google_id
        if password_plaintext != None:
            self.set_password(password_plaintext)

    def is_password_correct(self, password_plaintext):
        return check_password_hash(self.password_hashed, password_plaintext)

    def set_password(self, password_plaintext):
        if not password_plaintext:
            raise AssertionError("Mot de passe manquant")

        if len(password_plaintext) < 8 or len(password_plaintext) > 70:
            raise AssertionError("Le mot de passe doit être entre 8 et 50 caractères")

        password_pattern = (
            "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        )

        if not re.match(password_pattern, password_plaintext):
            raise AssertionError(
                "Le mot de passe doit faire au moins 8 caractères et contenir au moins 1 caractère majuscule, 1 caractère minuscule, 1 chiffre et un caractère spécial"
            )

        self.password_hashed = generate_password_hash(password_plaintext)

    @validates("username")
    def validate_username(self, key, username):
        if not username:
            raise AssertionError("Pseudo manquant")

        if len(username) < 2 or len(username) > 50:
            raise AssertionError(
                "Le pseudo ne doit pas dépassé 50 caractères, ni en dessous de 2"
            )

        return username

    @validates("email")
    def validate_email(self, key, email):
        if not email:
            raise AssertionError("Email missing")

        if "@" not in email:
            raise AssertionError("Wrong email format")

        if len(email) < 2 or len(email) > 50:
            raise AssertionError("email must be between 2 and 50 characters")

        if not re.match("[^@]+@[^@]+.[^@]+", email):
            raise AssertionError("Provided email is not an email address")

        return email

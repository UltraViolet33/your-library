from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    IntegerField,
    EmailField,
)
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    pseudo = StringField("pseudo", validators=[DataRequired()])
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    password_confirmation = PasswordField(
        "password_confirmation", validators=[DataRequired()]
    )


class LoginForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class SearchBookForm(FlaskForm):
    search = StringField("search", validators=[DataRequired()])


class ListForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])


class BookListForm(FlaskForm):
    lists = SelectMultipleField(validators=[DataRequired()])


class PostForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    content = TextAreaField(validators=[DataRequired()])
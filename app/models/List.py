from .. import db


lists_books_table = db.Table(
    "lists_books",
    db.Column("list_id", db.Integer, db.ForeignKey("lists.id")),
    db.Column("book_id", db.Integer, db.ForeignKey("books.id")),
)


class List(db.Model):
    __tablename__ = "lists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    
    books = db.relationship(
        "Book", secondary=lists_books_table, backref="lists"
    )

    def __init__(self, name):
        self.name = name

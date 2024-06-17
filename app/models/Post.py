from .. import db

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())

    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    
    book_id = db.Column(db.Integer, db.ForeignKey(
        "books.id", ondelete="CASCADE"), nullable=False)
    
    def __init__(self, title, content, user_id, book_id):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.book_id = book_id
 

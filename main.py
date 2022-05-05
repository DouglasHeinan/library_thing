from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return "<Book {self.title}>"


db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    # for book in all_books:
        # title = book.title
        # author = book.author
        # rating = book.rating
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        create_entry(request.form)
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit_rating", methods=["GET", "POST"])
def edit_rating():
    if request.method == "POST":
        book_id = request.form["id"]
        book = Book.query.get(book_id)
        book.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for("home"))
    book_id = request.args.get("book_id")
    book = Book.query.get(book_id)
    return render_template("edit_rating.html", book=book)


@app.route("/delete")
def delete_entry():
    book_id = request.args.get("book_id")
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))


def create_entry(book):
    title = book["title"]
    author = book["author"]
    rating = book["rating"]
    new_book = Book(title=title, author=author, rating=rating)
    db.session.add(new_book)
    db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)


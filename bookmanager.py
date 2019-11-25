import os

from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(80),unique=True, nullable=False)
    author = db.Column(db.String(80))
    publisher = db.Column(db.String(80))

    def __repr__(self):
        return "<Title: {}>".format(self.title)

@app.route("/", methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        try:
            book = Book(
                title=request.form.get("title"),
                author=request.form.get('author'),
                publisher=request.form.get('publisher')
                )
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print('Failed to add book')
            print(e)
    books = Book.query.all()
    return render_template("home.html", books=books)


@app.route("/update", methods=["POST"])
def update():
    try:
        # Gets the old and updated title from the form 
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")

        newauthor = request.form.get("newauthor")
        #oldauthor = request.form.get("oldauthor")

        newpublisher = request.form.get("newpublisher")
        #oldpublisher= request.form.get("oldpublisher")

        # Fetches the book with the old title from the database
        book = Book.query.filter_by(title=oldtitle).first()

        # Updates that book's title to the new title
        book.title = newtitle
        book.author = newauthor
        book.publisher = newpublisher

        # Saves the book to the database
        db.session.commit()
    except Exception as e:
        print('Could not update book title')
        print(e)

    # Redirects the user the the main page
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
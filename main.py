from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///places.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Attractions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)


class Museums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)


class Parks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)


class InterestingPlaces(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/create_new_note", methods=['POST', 'GET'])
def create_new_note():
    if request.method == "POST":
        if request.form['what'] == '1':
            title = request.form['title']
            address = request.form['address']
            description = request.form['description']

            place = Attractions(title=title, address=address, description=description)
            try:
                db.session.add(place)
                db.session.commit()
                return redirect("/")
            except:
                return "Ошибка"

        if request.form['what'] == '2':
            title = request.form['title']
            address = request.form['address']
            description = request.form['description']

            place = Museums(title=title, address=address, description=description)
            try:
                db.session.add(place)
                db.session.commit()
                return redirect("/")
            except:
                return "Ошибка"

        if request.form['what'] == '3':
            title = request.form['title']
            address = request.form['address']
            description = request.form['description']

            place = Parks(title=title, address=address, description=description)
            try:
                db.session.add(place)
                db.session.commit()
                return redirect("/")
            except:
                return "Ошибка"

        if request.form['what'] == '4':
            title = request.form['title']
            address = request.form['address']
            description = request.form['description']

            place = InterestingPlaces(title=title, address=address, description=description)
            try:
                db.session.add(place)
                db.session.commit()
                return redirect("/")
            except:
                return "Ошибка"

    else:
        return render_template("create_new_note.html")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

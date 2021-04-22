from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user

app = Flask(__name__)
app.secret_key = 'some'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///places.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)  # подключение базы данных

login_manager = LoginManager()
login_manager.init_app(app)

# создание таблиц в базе данных


# таблица с информацией о достопримечательностях
class Attractions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)


# таблица с информацией о музеях
class Museums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)


# таблица с информацией о парках
class Parks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)


# таблица с информацией об интересных местах
class InterestingPlaces(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)


# таблица с информацией о пользователях
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


#  начальная страница: выбор регистрация или авторизация
@app.route("/")
def index():
    return render_template("index.html")


#  основная страница
@app.route("/main")
def main():
    return render_template("main.html")


#  страница, где можно добавить свою запись
@app.route("/create_new_note", methods=['POST', 'GET'])
def create_new_note():
    if request.method == "POST":
        #  если запись о достопримечательности, то она добавляется на соответсвующую страницу
        if request.form['what'] == '1':
            title = request.form['title']
            address = request.form['address']
            description = request.form['description']
            place = Attractions(title=title, address=address, description=description)
            try:
                db.session.add(place)
                db.session.flush()
                db.session.commit()
                return redirect("/main")
            except:
                db.session.rollback()
                return "Ошибка"

        #  если запись о музее, то она добавляется на соответсвующую страницу
        if request.form['what'] == '2':
            title = request.form['title']
            address = request.form['address']
            description = request.form['description']
            place = Museums(title=title, address=address, description=description)
            try:
                db.session.add(place)
                db.session.flush()
                db.session.commit()
                return redirect("/main")
            except:
                db.session.rollback()
                return "Ошибка"

        #  если запись о парке, то она добавляется на соответсвующую страницу
        if request.form['what'] == '3':
            title = request.form['title']
            address = request.form['address']
            description = request.form['description']
            place = Parks(title=title, address=address, description=description)
            try:
                db.session.add(place)
                db.session.flush()
                db.session.commit()
                return redirect("/main")
            except:
                db.session.rollback()
                return "Ошибка"

        #  если запись об интересном месте, то она добавляется на соответсвующую страницу
        if request.form['what'] == '4':
            title = request.form['title']
            address = request.form['address']
            description = request.form['description']
            place = InterestingPlaces(title=title, address=address, description=description)
            try:
                db.session.add(place)
                db.session.flush()
                db.session.commit()
                return redirect("/main")
            except:
                db.session.rollback()
                return "Ошибка"
    else:
        return render_template("create_new_note.html")


#  страница с записями о достопримечательностях
@app.route("/attractions")
def attractions():
    p = Attractions.query.all()
    return render_template("notes.html", data=p, title='Достопримечательности', h1='Достопримечательности')


#  страница с записями о музеях
@app.route("/museums")
def museums():
    p = Museums.query.all()
    return render_template("notes.html", data=p, title='Музеи', h1='Музеи')


#  страница с записями о парках
@app.route("/parks")
def parks():
    p = Parks.query.all()
    return render_template("notes.html", data=p, title='Парки', h1='Парки')


#  страница с записями об интересных местах
@app.route("/interesting_places")
def interesting_places():
    p = InterestingPlaces.query.all()
    return render_template("notes.html", data=p, title='Интересные места', h1='Интересные места')


#  страница с формой регистрации
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        hash = generate_password_hash(request.form["password"])
        name = request.form['name']
        email = request.form['email']
        u = Users(name=name, email=email, password=hash)
        try:
            db.session.add(u)
            db.session.flush()
            db.session.commit()
            return redirect("/main")
        except:
            db.session.rollback()
            return "Ошибка"
    return render_template("register.html")


#  страница с формой авторизации
@app.route("/login", methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        user = Users.query.filter_by(email=email).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect("/main")
        flash("Неверный  логин или пароль", "error")
    return render_template("login.html")


#  дополнительный метод для авторизации
@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for('login'))
    return response


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

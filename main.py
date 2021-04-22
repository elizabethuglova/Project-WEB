from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,login_user
from data import db_session
from data.users import Users
from data.interesting_places import InterestingPlaces
from data.parks import Parks
from data.museums import Museums
from data.attractions import Attractions


app = Flask(__name__)
app.secret_key = 'some'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db = db_session.create_session()
    return db.query(Users).get(user_id)


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
            db = db_session.create_session()
            place = Attractions(title=title, address=address, description=description)
            try:
                db.add(place)
                db.flush()
                db.commit()
                return redirect("/main")
            except:
                db.rollback()
                return "Ошибка"

        #  если запись о музее, то она добавляется на соответсвующую страницу
        if request.form['what'] == '2':
            title = request.form['title']
            address = request.form['address']
            description = request.form['description']
            db = db_session.create_session()
            place = Museums(title=title, address=address, description=description)
            try:
                db.add(place)
                db.flush()
                db.commit()
                return redirect("/main")
            except:
                db.rollback()
                return "Ошибка"

        #  если запись о парке, то она добавляется на соответсвующую страницу
        if request.form['what'] == '3':
            title = request.form['title']
            address = request.form['address']
            description = request.form['description']
            db = db_session.create_session()
            place = Parks(title=title, address=address, description=description)
            try:
                db.add(place)
                db.flush()
                db.commit()
                return redirect("/main")
            except:
                db.rollback()
                return "Ошибка"

        #  если запись об интересном месте, то она добавляется на соответсвующую страницу
        if request.form['what'] == '4':
            title = request.form['title']
            address = request.form['address']
            description = request.form['description']
            db = db_session.create_session()
            place = InterestingPlaces(title=title, address=address, description=description)
            try:
                db.add(place)
                db.flush()
                db.commit()
                return redirect("/main")
            except:
                db.rollback()
                return "Ошибка"
    else:
        return render_template("create_new_note.html")


#  страница с записями о достопримечательностях
@app.route("/attractions")
def attractions():
    db = db_session.create_session()
    p = db.query(Attractions).all()
    return render_template("notes.html", data=p, title='Достопримечательности', h1='Достопримечательности')


#  страница с записями о музеях
@app.route("/museums")
def museums():
    db = db_session.create_session()
    p = db.query(Museums).all()
    return render_template("notes.html", data=p, title='Музеи', h1='Музеи')


#  страница с записями о парках
@app.route("/parks")
def parks():
    db = db_session.create_session()
    p = db.query(Parks).all()
    return render_template("notes.html", data=p, title='Парки', h1='Парки')


#  страница с записями об интересных местах
@app.route("/interesting_places")
def interesting_places():
    db = db_session.create_session()
    p = db.query(InterestingPlaces).all()
    return render_template("notes.html", data=p, title='Интересные места', h1='Интересные места')


#  страница с формой регистрации
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        hash = generate_password_hash(request.form["password"])
        name = request.form['name']
        email = request.form['email']
        db = db_session.create_session()
        u = Users(name=name, email=email, password=hash)
        try:
            db.add(u)
            db.flush()
            db.commit()
            return redirect("/main")
        except:
            db.rollback()
            return "Ошибка"
    return render_template("register.html")


#  страница с формой авторизации
@app.route("/login", methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    db = db_session.create_session()
    if email and password:
        user = db.query(Users).filter_by(email=email).first()
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
    db_session.global_init("places.db")
    app.run(port=8080, host='127.0.0.1')

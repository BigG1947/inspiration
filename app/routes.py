import os

from app import app, db
from flask import render_template, request, session, redirect
from app.functions import upload_images
from app.models import News, Teacher, Direction

news1 = {
    'id': 1,
    'title': 'Новость1',
    'description': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aspernatur dolor enim esse '
                   'laboriosam, nam numquam odio, officia perspiciatis quaerat, rerum soluta tenetur veritatis '
                   'voluptatibus. Assumenda iure maxime minus optio placeat!',
    'img': '/static/img/news3.jpg',
    'text': '................',
    'author': 'Новикова А.Н.',
    'date': '12-01-2019'
}
news2 = {
    'id': 2,
    'title': 'Новость2',
    'description': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aspernatur dolor enim esse '
                   'laboriosam, nam numquam odio, officia perspiciatis quaerat, rerum soluta tenetur veritatis '
                   'voluptatibus. Assumenda iure maxime minus optio placeat!',
    'img': '/static/img/news1.jpg',
    'text': '................',
    'author': 'Новикова А.Н.',
    'date': '12-01-2019'
}
news3 = {
    'id': 3,
    'title': 'Новость3',
    'description': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aspernatur dolor enim esse '
                   'laboriosam, nam numquam odio, officia perspiciatis quaerat, rerum soluta tenetur veritatis '
                   'voluptatibus. Assumenda iure maxime minus optio placeat!',
    'img': '/static/img/news2.jpg',
    'text': '................',
    'author': 'Новикова А.Н.',
    'date': '12-01-2019'
}
news_list = [news1, news2, news3]


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", news_list=news_list)


@app.route('/news')
def news():
    return render_template('news.html', news_list=news_list)


@app.route("/news/<int:id>")
def single(id):
    return render_template('single.html', news=news3)


@app.route("/direction/<int:id>")
def direction(id):
    return render_template("direct.html")


@app.route("/logoped")
def logoped():
    return render_template("logoped.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


@app.route("/album/<int:id>")
def album(id):
    return render_template("album.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if 'admin' in session:
        return redirect("/admin", 302)
    login = ""
    password = ""
    error = ""
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]
        print(app.config)
        if login == app.config["LOGIN"] and password == app.config["PASSWORD"]:
            session['admin'] = login
            return redirect("/admin", 302)
        error = "Неверный логин или пароль"
        return render_template("admin/login.html", login=login, password=password, error=error)
    return render_template("admin/login.html", login=login, password=password, error=error)


@app.route("/logout")
def logout():
    session.pop('admin', None)
    return redirect("/", 302)


@app.route("/admin")
def admin():
    if 'admin' in session:
        news = News.query.all()
        return render_template("admin/index.html", news=news)
    return redirect("/login", 302)


# NEWS CONTROLLERS

@app.route("/admin/news/add", methods=["GET", "POST"])
def news_add():
    if 'admin' in session:
        title = ""
        text = ""
        img = ""
        id_teacher = 0
        error = ""
        if request.method == "POST":
            title = request.form['title']
            text = request.form['text']
            id_teacher = request.form['id_teacher']
            file = request.files.get('img', None)
            if file is None:
                error = "Необходимо выбрать файл!"
                return render_template("admin/news_form.html", title=title, text=text, img=img, id_teacher=id_teacher,
                                       error=error)
            ok, img = upload_images(file)
            if ok is not True:
                error = "Ошибка при загрузке фотографии!"
                return render_template("admin/news_form.html", title=title, text=text, img=img, id_teacher=id_teacher,
                                       error=error)
            news = News()
            news.title = title
            news.id_author = id_teacher
            news.img = img
            news.text = text
            news.add()
            return redirect("/admin", 302)
        return render_template("admin/news_form.html", title=title, text=text, img=img, id_teacher=id_teacher, error=error)
    return redirect("/login", 302)


@app.route("/admin/news/<int:id>/edit", methods=["GET", "POST"])
def news_edit(id):
    if 'admin' in session:
        error = ""
        news = News.query.get(id)
        if request.method == "POST":
            news.title = request.form['title']
            news.text = request.form['text']
            news.id_author = request.form['id_teacher']
            file = request.files.get('img', None)
            if file is not None:
                print("new images")
                ok, news.img = upload_images(file, news.img)
                print(news.img)
                print(ok)
                if ok is not True:
                    error = "Ошибка при загрузке фотографии!"
                    return render_template("admin/news_form.html", title=news.title, text=news.text, img=news.img, id_teacher=news.id_author,
                                           error=error)
            news.edit()
            return redirect("/admin", 302)
        return render_template("admin/news_form.html", title=news.title, text=news.text, img=news.img, id_teacher=news.id_author, error=error)
    return redirect("/login", 302)


@app.route("/admin/news/<int:id>/delete")
def news_delete(id):
    news = News.query.get(id) or None
    if news is not None:
        news.delete()
    return redirect("/admin", 302)

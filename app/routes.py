import json
from datetime import datetime

from app import app, db
from flask import render_template, request, session, redirect, make_response, flash
from app.functions import upload_images, delete_un_use_image
from app.models import News, Teacher, Direction, Album, FreeLesson


@app.route("/")
@app.route("/index")
def index():
    news = News.query.order_by(News.date.desc(), News.id.desc()).all()
    directions = Direction.query.order_by(Direction.id.desc()).all()
    albums = Album.query.order_by(Album.date.desc(), Album.id.desc()).all()
    free_lesson = request.cookies.get('free_lesson')
    return render_template("index.html", news_list=news, directions=directions, albums=albums, free_lesson=free_lesson)


@app.route('/news')
def news():
    news = News.query.order_by(News.date.desc())
    return render_template('news.html', news_list=news)


@app.route("/news/<int:id>")
def single(id):
    news = News.query.get(id)
    if news is None:
        return redirect("/404", 302)
    return render_template('single.html', news=news)


@app.route("/direction/<int:id>")
def direction(id):
    direction = Direction.query.get(id) or None
    if direction is None:
        return redirect("/#main-directions", 302)
    return render_template("direct.html", direction=direction, images_list=json.loads(direction.images))


@app.route("/logoped")
def logoped():
    return render_template("logoped.html")


@app.route("/gallery")
def gallery():
    albums = Album.query.order_by(Album.date.desc(), Album.id.desc()).all()
    return render_template("gallery.html", albums=albums)


@app.route("/album/<int:id>")
def album(id):
    album = Album.query.get(id)
    return render_template("album.html", album=album, images=json.loads(album.images))


@app.route("/lesson/feedback", methods=["POST"])
def lesson_feedback():
    if 'admin' in session:
        return redirect("/admin", 302)
    free_lesson = FreeLesson()
    free_lesson.parent_name = request.form["parent_name"]
    free_lesson.parent_number = request.form["parent_number"]
    free_lesson.child_name = request.form["child_name"]
    free_lesson.id_direction = request.form["id_direction"]
    free_lesson.add()
    flash("Заявка на бесплатный урок успешно отправленна!")
    response = make_response(redirect("/#main-free-lesson", 302))
    response.set_cookie("free_lesson", 'true', max_age=60 * 60 * 24)
    return response


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
        news = News.query.order_by(News.id.desc()).all()
        teachers = Teacher.query.order_by(Teacher.id.desc()).all()
        directions = Direction.query.order_by(Direction.id.desc()).all()
        albums = Album.query.order_by(Album.id.desc()).all()
        new_feedbacks = FreeLesson.query.filter_by(is_view=False).order_by(FreeLesson.date.desc(),
                                                                           FreeLesson.id.desc()).all()
        old_feedbacks = FreeLesson.query.filter_by(is_view=True).order_by(FreeLesson.date.desc(),
                                                                          FreeLesson.id.desc()).all()
        return render_template("admin/index.html", new_feedbacks=new_feedbacks, old_feedbacks=old_feedbacks, news=news,
                               teachers=teachers, directions=directions, albums=albums)
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
        teachers = Teacher.query.order_by(Teacher.fio.asc())
        if request.method == "POST":
            title = request.form['title']
            text = request.form['text']
            id_teacher = request.form['id_teacher']
            file = request.files.get('img', None)
            if file is None:
                error = "Необходимо выбрать файл!"
                return render_template("admin/news_form.html", title=title, text=text, img=img, id_teacher=id_teacher,
                                       teachers=teachers, error=error)
            ok, img = upload_images(file)
            if ok is not True:
                error = "Ошибка при загрузке фотографии!"
                return render_template("admin/news_form.html", title=title, text=text, img=img, id_teacher=id_teacher,
                                       teachers=teachers, error=error)
            news = News()
            news.title = title
            news.id_author = id_teacher
            news.img = img
            news.text = text
            news.add()
            return redirect("/admin", 302)
        return render_template("admin/news_form.html", title=title, text=text, img=img, id_teacher=id_teacher,
                               teachers=teachers, error=error)
    return redirect("/login", 302)


@app.route("/admin/news/<int:id>/edit", methods=["GET", "POST"])
def news_edit(id):
    if 'admin' in session:
        error = ""
        news = News.query.get(id)
        teachers = Teacher.query.order_by(Teacher.fio.asc())
        if request.method == "POST":
            news.title = request.form['title']
            news.text = request.form['text']
            news.id_author = request.form['id_teacher']
            file = request.files.get('img', None)
            if file is not None:
                ok, news.img = upload_images(file, news.img)
                if ok is not True:
                    error = "Ошибка при загрузке фотографии!"
                    return render_template("admin/news_form.html", title=news.title, text=news.text, img=news.img,
                                           id_teacher=news.id_author,
                                           teachers=teachers, error=error)
            news.edit()
            return redirect("/admin", 302)
        return render_template("admin/news_form.html", title=news.title, text=news.text, img=news.img,
                               teachers=teachers, id_teacher=news.id_author, error=error)
    return redirect("/login", 302)


@app.route("/admin/news/<int:id>/delete")
def news_delete(id):
    if 'admin' in session:
        news = News.query.get(id) or None
        if news is not None:
            delete_un_use_image(news.img)
            news.delete()
        return redirect("/admin", 302)
    return redirect("/login", 302)


# TEACHERS CONTROLLER
@app.route("/admin/teachers/add", methods=["GET", "POST"])
def teachers_add():
    if 'admin' in session:
        directions = Direction.query.order_by(Direction.id.desc()).all()
        error = ""
        fio = ""
        photo = ""
        position = ""
        id_direction = ""
        birthday = ""
        if request.method == "POST":
            fio = request.form["fio"]
            position = request.form["position"]
            id_direction = request.form["id_direction"]
            birthday = request.form["birthday"]
            file = request.files.get("photo", None)
            if file is None:
                error = "Необходимо выбрать фотографию!"
                return render_template("admin/teachers_form.html", error=error, fio=fio, photo=photo, position=position,
                                       id_direction=id_direction, birthday=birthday, directions=directions)
            ok, photo = upload_images(file)
            if ok is not True:
                error = "Ошибка при загрузке фотографии!"
                return render_template("admin/teachers_form.html", error=error, fio=fio, photo=photo, position=position,
                                       id_direction=id_direction, birthday=birthday, directions=directions)
            teacher = Teacher()
            teacher.fio = fio
            teacher.birthday = datetime.strptime(birthday, '%Y-%m-%d')
            teacher.id_direction = id_direction
            teacher.position = position
            teacher.photo = photo
            teacher.add()
            return redirect("/admin", 302)
        return render_template("admin/teachers_form.html", error=error, fio=fio, photo=photo, position=position,
                               id_direction=id_direction, birthday=birthday, directions=directions)
    return redirect("/login", 302)


@app.route("/admin/teachers/<int:id>/edit", methods=["GET", "POST"])
def teachers_edit(id):
    if 'admin' in session:
        error = ""
        teacher = Teacher.query.get(id)
        directions = Direction.query.all()
        if request.method == "POST":
            teacher.fio = request.form["fio"]
            teacher.position = request.form["position"]
            teacher.id_direction = request.form["id_direction"]
            teacher.birthday = datetime.strptime(request.form["birthday"], '%Y-%m-%d')
            file = request.files.get("photo", None)
            if file is not None:
                ok, teacher.photo = upload_images(file, teacher.photo)
                if ok is not True:
                    error = "Ошибка при загрузке фотографии!"
                    return render_template("admin/teachers_form.html", error=error, fio=teacher.fio,
                                           photo=teacher.photo, position=teacher.position,
                                           id_direction=teacher.id_direction, birthday=teacher.birthday,
                                           directions=directions)
            teacher.edit()
            return redirect("/admin", 302)
        return render_template("admin/teachers_form.html", error=error, fio=teacher.fio, photo=teacher.photo,
                               position=teacher.position,
                               id_direction=teacher.id_direction, birthday=teacher.birthday, directions=directions)
    return redirect("/login", 302)


@app.route("/admin/teachers/<int:id>/delete")
def teachers_delete(id):
    if 'admin' in session:
        teacher = Teacher.query.get(id) or None
        if teacher is not None:
            delete_un_use_image(teacher.photo)
            teacher.delete()
        return redirect("/admin", 302)
    return redirect("/login", 302)


# DIRECTION CONTROLLER
@app.route("/admin/direction/add", methods=["GET", "POST"])
def direction_add():
    if 'admin' in session:
        name = ""
        description = ""
        main_image = ""
        images = []
        error = ""
        if request.method == "POST":
            name = request.form['name']
            description = request.form['description']
            file = request.files.get("main_image", None)
            if file is None:
                error = "Необходимо выбрать главное изображение!"
                return render_template("admin/direction_form.html", error=error, name=name, description=description,
                                       main_image=main_image, images=images)
            ok, main_image = upload_images(file)
            if ok is not True:
                error = "Ошибка при загрузке фотографии!"
                return render_template("admin/direction_form.html", error=error, name=name, description=description,
                                       main_image=main_image, images=images)
            images_form = request.files.getlist("images")
            if images_form:
                for image in images_form:
                    ok, path = upload_images(image)
                    if ok is not True:
                        error = "Ошибка при загрузке фотографии!"
                        return render_template("admin/direction_form.html", error=error, name=name,
                                               description=description,
                                               main_image=main_image, images=images)
                    images.append(path)
            direction = Direction()
            direction.name = name
            direction.description = description
            direction.main_image = main_image
            direction.images = json.dumps(images)
            direction.add()
            return redirect("/admin", 302)
        return render_template("admin/direction_form.html", error=error, name=name, description=description,
                               main_image=main_image, images=images)
    return redirect("/login", 302)


@app.route("/admin/direction/<int:id>/edit", methods=["GET", "POST"])
def direction_edit(id):
    if 'admin' in session:
        error = ""
        images = []
        direction = Direction.query.get(id)
        if request.method == "POST":
            direction.name = request.form['name']
            direction.description = request.form['description']
            file = request.files.get("main_image")
            if file is not None:
                ok, direction.main_image = upload_images(file, direction.main_image)
                if ok is not True:
                    error = "Ошибка при загрузке фотографии2!"
                    return render_template("admin/direction_form.html", error=error, id=direction.id,
                                           name=direction.name, description=direction.description,
                                           main_image=direction.main_image, images=json.loads(direction.images))
            images_form = request.files.getlist("images")
            if images_form:
                for image in images_form:
                    ok, path = upload_images(image)
                    if ok is not True:
                        error = "Ошибка при загрузке фотографии!"
                        return render_template("admin/direction_form.html", error=error, id=direction.id,
                                               name=direction.name,
                                               description=direction.description,
                                               main_image=direction.main_image, images=json.loads(direction.images))
                    images.append(path)
                direction.images = json.dumps(json.loads(direction.images) + images)
            direction.edit()
            return redirect("/admin", 302)
        return render_template("admin/direction_form.html", error=error, id=direction.id, name=direction.name,
                               description=direction.description,
                               main_image=direction.main_image, images=json.loads(direction.images))
    return redirect("/login", 302)


@app.route("/admin/direction/<int:id>/delete")
def direction_delete(id):
    if 'admin' in session:
        direction = Direction.query.get(id) or None
        if direction is not None:
            delete_un_use_image(direction.main_image)
            images_list = json.loads(direction.images)
            for image in images_list:
                delete_un_use_image(image)
            direction.delete()
        return redirect("/admin", 302)
    return redirect("/login", 302)


@app.route("/admin/direction/images/delete/", methods=["POST"])
def direction_images_delete():
    if 'admin' in session:
        id = request.form['id']
        path = request.form['path']
        direction = Direction.query.get(id)
        if direction.images:
            images_list = json.loads(direction.images)
            for img in images_list:
                if img == path:
                    delete_un_use_image(path)
            images_list.remove(path)
            direction.images = json.dumps(images_list)
            direction.edit()
        return redirect("/admin/direction/{}/edit".format(id), 302)
    return redirect("/login", 302)


# ALBUM CONTROLLER
@app.route("/admin/album/add", methods=["GET", "POST"])
def album_add():
    if 'admin' in session:
        name = ""
        main_image = ""
        images = []
        error = ""
        if request.method == "POST":
            name = request.form['name']
            file = request.files.get("main_image", None)
            if file is None:
                error = "Необходимо выбрать главное изображение!"
                return render_template("admin/album_form.html", error=error, name=name, main_image=main_image,
                                       images=images)
            ok, main_image = upload_images(file)
            if ok is not True:
                error = "Ошибка при загрузке фотографии!"
                return render_template("admin/album_form.html", error=error, name=name, main_image=main_image,
                                       images=images)
            images_form = request.files.getlist("images")
            if images_form:
                for image in images_form:
                    ok, path = upload_images(image)
                    if ok is not True:
                        error = "Ошибка при загрузке фотографии!"
                        return render_template("admin/album_form.html", error=error, name=name,
                                               main_image=main_image, images=images)
                    images.append(path)
            album = Album()
            album.name = name
            album.main_image = main_image
            album.images = json.dumps(images)
            album.add()
            return redirect("/admin", 302)
        return render_template("admin/album_form.html")
    return redirect("/login", 302)


@app.route("/admin/album/<int:id>/edit", methods=["GET", "POST"])
def album_edit(id):
    if 'admin' in session:
        error = ""
        images = []
        album = Album.query.get(id)
        if request.method == "POST":
            album.name = request.form['name']
            file = request.files.get("main_image")
            if file is not None:
                ok, album.main_image = upload_images(file, album.main_image)
                if ok is not True:
                    error = "Ошибка при загрузке фотографии2!"
                    return render_template("admin/album_form.html", error=error, id=album.id,
                                           name=album.name,
                                           main_image=album.main_image, images=json.loads(album.images))
            images_form = request.files.getlist("images")
            if images_form:
                for image in images_form:
                    ok, path = upload_images(image)
                    if ok is not True:
                        error = "Ошибка при загрузке фотографии!"
                        return render_template("admin/album_form.html", error=error, id=album.id,
                                               name=album.name,
                                               main_image=album.main_image, images=json.loads(album.images))
                    images.append(path)
                album.images = json.dumps(json.loads(album.images) + images)
            album.edit()
            return redirect("/admin", 302)
        return render_template("admin/album_form.html", error=error, id=album.id,
                               name=album.name,
                               main_image=album.main_image, images=json.loads(album.images))
    return redirect("/login", 302)


@app.route("/admin/album/<int:id>/delete", methods=["GET", "POST"])
def album_delete(id):
    if 'admin' in session:
        album = Album.query.get(id) or None
        if album is not None:
            delete_un_use_image(album.main_image)
            images_list = json.loads(album.images)
            for image in images_list:
                delete_un_use_image(image)
            album.delete()
        return redirect("/admin", 302)
    return redirect("/login", 302)


@app.route("/admin/album/images/delete/", methods=["POST"])
def album_images_delete():
    if 'admin' in session:
        id = request.form['id']
        path = request.form['path']
        album = Album.query.get(id)
        if album.images:
            images_list = json.loads(album.images)
            for img in images_list:
                if img == path:
                    delete_un_use_image(path)
            images_list.remove(path)
            album.images = json.dumps(images_list)
            album.edit()
        return redirect("/admin/album/{}/edit".format(id), 302)
    return redirect("/login", 302)


@app.route("/admin/free_lesson/<int:id>/view")
def free_lesson_view(id):
    if 'admin' in session:
        free_lesson = FreeLesson.query.get(id)
        free_lesson.is_view = True
        free_lesson.edit()
        return redirect("/admin", 302)
    return redirect("/login", 302)

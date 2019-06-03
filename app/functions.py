import os
from app.models import News, Teacher, Direction, Album


def upload_images(file, old_img=None):
    if old_img:
        result_news = News.query.filter_by(img=old_img).all()
        result_teacher = Teacher.query.filter_by(photo=old_img).all()
        result_direction = Direction.query.filter_by(main_image=old_img).all()
        result_second_direction = Direction.query.filter(Direction.images.like("%{}%".format(old_img))).all()
        result_album = Album.query.filter_by(main_image=old_img).all()
        result_second_album = Album.query.filter(Album.images.like("%{}%".format(old_img))).all()

        total_score = len(result_teacher) + len(result_news) + len(result_direction) + len(
            result_second_direction) + len(result_album) + len(result_second_album)

        if total_score <= 1:
            if os.path.exists('app' + old_img):
                os.remove('app' + old_img)

    path = "/static/upload_images/" + file.filename
    file.save('app' + path)
    return True, path


def delete_un_use_image(path):
    result_news = News.query.filter_by(img=path).all()
    result_teacher = Teacher.query.filter_by(photo=path).all()
    result_direction = Direction.query.filter_by(main_image=path).all()
    result_second_direction = Direction.query.filter(Direction.images.like("%{}%".format(path))).all()
    result_album = Album.query.filter_by(main_image=path).all()
    result_second_album = Album.query.filter(Album.images.like("%{}%".format(path))).all()

    total_score = len(result_teacher) + len(result_news) + len(result_direction) + len(
        result_second_direction) + len(result_album) + len(result_second_album)

    if total_score <= 1:
        if os.path.exists('app' + path):
            os.remove('app' + path)

    return True

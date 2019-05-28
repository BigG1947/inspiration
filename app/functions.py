import os
from app.models import News, Teacher, Direction


def upload_images(file, old_img=None):
    if old_img:
        result_news = News.query.filter_by(img=old_img).all()
        result_teacher = Teacher.query.filter_by(photo=old_img).all()

        if len(result_teacher) <= 1 and len(result_news) <= 1:
            try:
                os.remove('app' + old_img)
            except OSError:
                return False, None

    path = "/static/upload_images/" + file.filename
    file.save('app' + path)
    return True, path


def delete_un_use_image(path):
    result_news = News.query.filter_by(img=path).all()
    result_teacher = Teacher.query.filter_by(photo=path).all()
    result_direction = Direction.query.filter_by(main_image=path).all()

    if len(result_teacher) <= 1 and len(result_news) <= 1 and len(result_direction) <= 1:
        try:
            os.remove('app' + path)
        except OSError:
            return False
    return True

from datetime import datetime

from app import db


class News(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    title = db.Column(db.String(256), nullable=False, unique=True)
    img = db.Column(db.String(512), nullable=False)
    id_author = db.Column(db.Integer, db.ForeignKey("teacher.id"))
    text = db.Column(db.Text)
    date = db.Column(db.Date, default=datetime.now().date())

    def add(self):
        db.session.add(self)
        db.session.commit()

    def edit(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Direction(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(256), nullable=False, unique=True)
    description = db.Column(db.Text)
    main_image = db.Column(db.String(512), nullable=False)
    images = db.Column(db.Text)
    teachers = db.relationship("Teacher", backref="direction", lazy="dynamic")


class Teacher(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    fio = db.Column(db.String(256), nullable=False)
    photo = db.Column(db.String(512), nullable=False)
    id_direction = db.Column(db.Integer, db.ForeignKey("direction.id"))
    position = db.Column(db.String(128), nullable=False)
    news = db.relationship("News", backref="author", lazy="dynamic")
    birthday = db.Column(db.Date, nullable=False)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def edit(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
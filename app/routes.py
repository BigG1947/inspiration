from app import app
from flask import render_template

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

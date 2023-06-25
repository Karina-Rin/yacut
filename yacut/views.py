# yacut/yacut/views.py

import random
import string

from flask import flash, redirect, render_template

from yacut.forms import URL_Form
from yacut.models import URLMap

from yacut import app, db


def get_db_object(column, query):
    """Фильтрация и получение ответа из БД."""
    return URLMap.query.filter(column == query)


def check_short_id(short_id):
    """Проверка уникальности нового адреса."""
    if get_db_object(URLMap.short, short_id).first() is None:
        return True
    return False


def get_unique_short_id():
    """Формирование коротких идентификаторов переменной длины."""
    short_id = "".join(random.choice(string.ascii_letters + string.digits) for i in range(6))
    if check_short_id(short_id):
        return short_id
    return get_unique_short_id()


@app.route("/", methods=["GET", "POST"])
def index_view():
    """Функция gозволяет пользователям сокращать заданный URL-адрес."""
    form = URL_Form()
    if not form.validate_on_submit():
        return render_template("index.html", form=form)
    custom_id = form.custom_id.data
    if not custom_id:
        custom_id = get_unique_short_id()
    elif not check_short_id(custom_id):
        flash(f"Имя {custom_id} уже занято!", "link-taken")
        return render_template("index.html", form=form)
    new_url = URLMap(original=form.original_link.data, short=custom_id)
    db.session.add(new_url)
    db.session.commit()
    return render_template("index.html", url=new_url, form=form)


@app.route("/<short_id>", methods=["GET"])
def follow_link(short_id):
    """Перенаправление на исходный URL-адрес для заданного короткого идентификатора."""
    db_object = URLMap.query.filter_by(short=short_id).first_or_404()
    original_link = db_object.original
    return redirect(original_link)

# yacut/yacut/error_handlers.py

from http import HTTPStatus

from flask import jsonify, render_template

from yacut import app, db


class APIErrors(Exception):
    """Пользовательский класс исключений для ошибок API."""

    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        """Инициализирует новый экземпляр класса ошибок API."""
        super().__init__
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Возвращает сообщение об ошибке в виде словаря."""
        return dict(message=self.message)


@app.errorhandler(APIErrors)
def api_errors(error):
    """Возвращает в ответе текст ошибки и статус-код."""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    """Обрабатывает ошибки 404 и возвращает пользовательскую страницу с ошибкой 404."""
    return render_template("404.html"), HTTPStatus.NOT_FOUND


@app.errorhandler(500)
def internal_error(error):
    """Обрабатывает ошибку 500 и возвращает пользовательскую страницу с ошибкой 500 при откате сеанса работы с базой данных."""
    db.session.rollback()
    return render_template("500.html"), HTTPStatus.INTERNAL_SERVER_ERROR
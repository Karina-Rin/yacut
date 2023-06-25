# yacut/yacut/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


class URL_Form(FlaskForm):
    """Класс создания формы сокращения URL."""

    original_link = URLField(
        "Оригинальная длинная ссылка",
        validators=[
            DataRequired(message="Обязательное поле"),
            URL(message="Некорректная ссылка"),
        ],
    )
    custom_id = StringField(
        "Пользовательский вариант короткой ссылки",
        validators=[
            Optional(),
            Length(1, 16),
            Regexp(
                regex=r'^[a-zA-Z\d]{1,16}$', message='Допустимы только цифры и буквы "a-Z"'
            ),
        ],
    )
    submit = SubmitField("Создать")

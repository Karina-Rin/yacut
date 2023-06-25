# yacut/yacut/models.py

from datetime import datetime as dt

from flask import url_for

from yacut import db


class URLMap(db.Model):
    """Сопоставление исходного URL-адрес с его сокращенной версией."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)

    def from_dict(self, data):
        """Заполнение поля объекта из словаря входных данных."""
        for field_db, field_inp in {'original': 'url', 'short': 'custom_id'}.items():
            if field_inp in data:
                setattr(self, field_db, data[field_inp])

    def to_dict(self):
        """Преобразование объекта в словарное представление в формате JSON."""
        return dict(
            url=self.original,
            short_link=url_for("index_view", _external=True) + self.short,
        )

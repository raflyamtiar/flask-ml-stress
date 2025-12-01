from datetime import datetime
from typing import Optional

from flask import current_app

from . import db


class AppInfo(db.Model):
    __tablename__ = 'app_info'

    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(255), nullable=False)
    app_version = db.Column(db.String(64))
    description = db.Column(db.Text)
    owner = db.Column(db.String(128))
    contact = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


class HistoryStress(db.Model):
    __tablename__ = 'stress_history'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    hr = db.Column(db.Float)
    temp = db.Column(db.Float)
    eda = db.Column(db.Float)
    label = db.Column(db.String(128))
    confidence_level = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


def create_tables(app=None) -> None:
    """Create database tables using SQLAlchemy's metadata.

    Call with an application instance or call from within an app context.
    """
    if app is not None:
        with app.app_context():
            db.create_all()
    else:
        # Try current_app context
        with current_app.app_context():
            db.create_all()


__all__ = ["AppInfo", "HistoryStress", "create_tables"]


if __name__ == '__main__':
    # Initialize using Flask app factory so SQLALCHEMY_DATABASE_URI is honored
    from . import create_app

    app = create_app()
    print('Initializing database (SQLAlchemy)...')
    create_tables(app)
    print('Done')

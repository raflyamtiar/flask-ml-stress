from datetime import datetime, timezone, timedelta
from typing import Optional
import uuid

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

# Jakarta timezone (UTC+7)
JAKARTA_TZ = timezone(timedelta(hours=7))


class AppInfo(db.Model):
    __tablename__ = 'app_info'

    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(255), nullable=False)
    app_version = db.Column(db.String(64))
    description = db.Column(db.Text)
    owner = db.Column(db.String(128))
    contact = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(JAKARTA_TZ))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(JAKARTA_TZ), onupdate=lambda: datetime.now(JAKARTA_TZ))


class MeasurementSession(db.Model):
    """Model for measurement sessions. Each session groups related stress measurements."""
    __tablename__ = 'measurement_sessions'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)
    
    # Relationships with cascade delete
    stress_histories = db.relationship('HistoryStress', back_populates='session', lazy='dynamic', cascade='all, delete-orphan')
    sensor_readings = db.relationship('SensorReading', back_populates='session', lazy='dynamic', cascade='all, delete-orphan')


class HistoryStress(db.Model):
    __tablename__ = 'stress_history'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey('measurement_sessions.id', ondelete='CASCADE'), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    hr = db.Column(db.Float)
    temp = db.Column(db.Float)
    eda = db.Column(db.Float)
    label = db.Column(db.String(128))
    confidence_level = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(JAKARTA_TZ))
    
    # Relationship
    session = db.relationship('MeasurementSession', back_populates='stress_histories')


class SensorReading(db.Model):
    """Model for storing individual sensor readings within a measurement session."""
    __tablename__ = 'sensor_readings'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey('measurement_sessions.id', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    hr = db.Column(db.Float, nullable=False)
    temp = db.Column(db.Float, nullable=False)
    eda = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(JAKARTA_TZ))
    
    # Relationship
    session = db.relationship('MeasurementSession', back_populates='sensor_readings')


class User(db.Model):
    """Model for user authentication and authorization."""
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(JAKARTA_TZ))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(JAKARTA_TZ), onupdate=lambda: datetime.now(JAKARTA_TZ))

    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_timestamps: bool = True) -> dict:
        """Convert user object to dictionary (excluding password)."""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
        if include_timestamps:
            data['created_at'] = self.created_at.isoformat() if self.created_at else None
            data['updated_at'] = self.updated_at.isoformat() if self.updated_at else None
        return data

    def __repr__(self):
        return f'<User {self.username}>'


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


__all__ = ["AppInfo", "MeasurementSession", "HistoryStress", "SensorReading", "User", "create_tables"]


if __name__ == '__main__':
    # Initialize using Flask app factory so SQLALCHEMY_DATABASE_URI is honored
    from . import create_app

    app = create_app()
    print('Initializing database (SQLAlchemy)...')
    create_tables(app)
    print('Done')

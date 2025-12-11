from datetime import datetime
from typing import Optional
import uuid

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


class MeasurementSession(db.Model):
    """Model for measurement sessions. Each session groups related stress measurements."""
    __tablename__ = 'measurement_sessions'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)
    
    # Relationships
    stress_histories = db.relationship('HistoryStress', back_populates='session', lazy='dynamic')
    sensor_readings = db.relationship('SensorReading', back_populates='session', lazy='dynamic')


class HistoryStress(db.Model):
    __tablename__ = 'stress_history'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey('measurement_sessions.id'), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    hr = db.Column(db.Float)
    temp = db.Column(db.Float)
    eda = db.Column(db.Float)
    label = db.Column(db.String(128))
    confidence_level = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relationship
    session = db.relationship('MeasurementSession', back_populates='stress_histories')


class SensorReading(db.Model):
    """Model for storing individual sensor readings within a measurement session."""
    __tablename__ = 'sensor_readings'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey('measurement_sessions.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    hr = db.Column(db.Float, nullable=False)
    temp = db.Column(db.Float, nullable=False)
    eda = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relationship
    session = db.relationship('MeasurementSession', back_populates='sensor_readings')


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


__all__ = ["AppInfo", "MeasurementSession", "HistoryStress", "SensorReading", "create_tables"]


if __name__ == '__main__':
    # Initialize using Flask app factory so SQLALCHEMY_DATABASE_URI is honored
    from . import create_app

    app = create_app()
    print('Initializing database (SQLAlchemy)...')
    create_tables(app)
    print('Done')

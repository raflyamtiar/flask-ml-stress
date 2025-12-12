from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
from flask_jwt_extended import create_access_token, create_refresh_token
from . import db
from .models import AppInfo, HistoryStress, MeasurementSession, SensorReading, User
import os
from pathlib import Path
import joblib
import pandas as pd
import uuid

# Jakarta timezone (UTC+7)
JAKARTA_TZ = timezone(timedelta(hours=7))


class AppInfoService:
    """Service class for handling app_info CRUD operations."""

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all app info records."""
        app_infos = AppInfo.query.all()
        return [AppInfoService._to_dict(app_info) for app_info in app_infos]

    @staticmethod
    def get_by_id(app_id: int) -> Optional[Dict[str, Any]]:
        """Get an app info record by ID."""
        app_info = AppInfo.query.get(app_id)
        return AppInfoService._to_dict(app_info) if app_info else None

    @staticmethod
    def create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new app info record."""
        app_info = AppInfo(
            app_name=data['app_name'],
            app_version=data.get('app_version'),
            description=data.get('description'),
            owner=data.get('owner'),
            contact=data.get('contact')
        )
        db.session.add(app_info)
        db.session.commit()
        return AppInfoService._to_dict(app_info)

    @staticmethod
    def update(app_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing app info record."""
        app_info = AppInfo.query.get(app_id)
        if not app_info:
            return None

        # Update fields if provided
        if 'app_name' in data:
            app_info.app_name = data['app_name']
        if 'app_version' in data:
            app_info.app_version = data['app_version']
        if 'description' in data:
            app_info.description = data['description']
        if 'owner' in data:
            app_info.owner = data['owner']
        if 'contact' in data:
            app_info.contact = data['contact']
        
        # Use Jakarta time
        app_info.updated_at = datetime.now(JAKARTA_TZ)
        db.session.commit()
        return AppInfoService._to_dict(app_info)

    @staticmethod
    def delete(app_id: int) -> bool:
        """Delete an app info record."""
        app_info = AppInfo.query.get(app_id)
        if not app_info:
            return False

        db.session.delete(app_info)
        db.session.commit()
        return True

    @staticmethod
    def _to_dict(app_info: AppInfo) -> Dict[str, Any]:
        """Convert AppInfo model to dictionary."""
        return {
            'id': app_info.id,
            'app_name': app_info.app_name,
            'app_version': app_info.app_version,
            'description': app_info.description,
            'owner': app_info.owner,
            'contact': app_info.contact,
            'created_at': app_info.created_at.isoformat() if app_info.created_at else None,
            'updated_at': app_info.updated_at.isoformat() if app_info.updated_at else None
        }


class StressHistoryService:
    """Service class for handling stress_history CRUD operations."""

    @staticmethod
    def get_all():
        histories = HistoryStress.query.order_by(HistoryStress.timestamp.desc()).all()
        return [StressHistoryService._to_dict(h) for h in histories]

    @staticmethod
    def get_by_id(rec_id: int):
        rec = HistoryStress.query.get(rec_id)
        return StressHistoryService._to_dict(rec) if rec else None

    @staticmethod
    def get_by_session(session_id: str) -> List[Dict[str, Any]]:
        """Get all stress history records for a specific session."""
        histories = HistoryStress.query.filter_by(session_id=session_id).order_by(HistoryStress.timestamp.desc()).all()
        return [StressHistoryService._to_dict(h) for h in histories]

    @staticmethod
    def create(data: dict):
        # Use Jakarta time for timestamp
        ts_val = datetime.now(JAKARTA_TZ)

        rec = HistoryStress(
            timestamp=ts_val,
            session_id=data.get('session_id'),
            hr=data.get('hr'),
            temp=data.get('temp'),
            eda=data.get('eda'),
            label=data.get('label'),
            confidence_level=data.get('confidence_level'),
            notes=data.get('notes') or ''
        )
        db.session.add(rec)
        db.session.commit()
        return StressHistoryService._to_dict(rec)

    @staticmethod
    def update(rec_id: int, data: dict):
        rec = HistoryStress.query.get(rec_id)
        if not rec:
            return None

        if 'timestamp' in data:
            try:
                # Parse timestamp and convert to Jakarta timezone
                parsed_ts = datetime.fromisoformat(data['timestamp'])
                # If timezone-aware, convert to Jakarta; if naive, assume Jakarta
                if parsed_ts.tzinfo is not None:
                    rec.timestamp = parsed_ts.astimezone(JAKARTA_TZ)
                else:
                    rec.timestamp = parsed_ts.replace(tzinfo=JAKARTA_TZ)
            except Exception:
                pass
        if 'hr' in data:
            rec.hr = data.get('hr')
        if 'temp' in data:
            rec.temp = data.get('temp')
        if 'eda' in data:
            rec.eda = data.get('eda')
        if 'label' in data:
            rec.label = data.get('label')
        if 'confidence_level' in data:
            rec.confidence_level = data.get('confidence_level')
        if 'notes' in data:
            rec.notes = data.get('notes')

        db.session.commit()
        return StressHistoryService._to_dict(rec)

    @staticmethod
    def delete(rec_id: int) -> bool:
        rec = HistoryStress.query.get(rec_id)
        if not rec:
            return False
        db.session.delete(rec)
        db.session.commit()
        return True

    @staticmethod
    def get_recent_count(hours: int = 24) -> int:
        """Get count of records from the last N hours."""
        from datetime import timedelta
        cutoff_time = datetime.now(JAKARTA_TZ) - timedelta(hours=hours)
        count = HistoryStress.query.filter(HistoryStress.timestamp >= cutoff_time).count()
        return count

    @staticmethod
    def _to_dict(rec: HistoryStress):
        return {
            'id': rec.id,
            'session_id': rec.session_id,
            'timestamp': rec.timestamp.isoformat() if rec.timestamp else None,
            'hr': rec.hr,
            'temp': rec.temp,
            'eda': rec.eda,
            'label': rec.label,
            'confidence_level': rec.confidence_level,
            'notes': rec.notes or '',
            'created_at': rec.created_at.isoformat() if rec.created_at else None
        }


class StressModelService:
    """Load ML scaler and model from repository `models/` folder and provide predict().

    Expects files:
      - models/scaler_model.pkl
      - models/classification_rf_model.pkl
    """

    _scaler = None
    _model = None

    @classmethod
    def _model_dir(cls) -> Path:
        # project root is parent of the `app` package
        return Path(__file__).resolve().parents[1] / 'models'

    @classmethod
    def _load_scaler(cls):
        if cls._scaler is None:
            scaler_path = cls._model_dir() / 'scaler_model.pkl'
            if not scaler_path.exists():
                raise RuntimeError(f"Scaler not found at {scaler_path}")
            cls._scaler = joblib.load(str(scaler_path))
        return cls._scaler

    @classmethod
    def _load_model(cls):
        if cls._model is None:
            model_path = cls._model_dir() / 'classification_rf_model.pkl'
            if not model_path.exists():
                raise RuntimeError(f"Model not found at {model_path}")
            cls._model = joblib.load(str(model_path))
        return cls._model

    @classmethod
    def predict(cls, hr: float, temp: float, eda: float) -> Dict[str, Any]:
        scaler = cls._load_scaler()
        model = cls._load_model()

        # prepare dataframe consistent with training columns
        df = pd.DataFrame([[hr, temp, eda]], columns=['HR', 'TEMP', 'EDA'])
        X = scaler.transform(df)

        pred = model.predict(X)[0]
        # probability for predicted class (max probability)
        try:
            proba = float(model.predict_proba(X).max())
        except Exception:
            # some models may not support predict_proba
            proba = 1.0

        label_dict = {0: 'Normal', 1: 'Medium', 2: 'High Stress'}
        label = label_dict.get(int(pred), str(pred))

        return {
            'hr': hr,
            'temp': temp,
            'eda': eda,
            'label': label,
            'confidence_level': proba
        }

class MeasurementSessionService:
    """Service class for handling measurement_sessions CRUD operations."""

    @staticmethod
    def create(data: dict = None) -> Dict[str, Any]:
        """Create a new measurement session."""
        session = MeasurementSession(
            id=str(uuid.uuid4()),
            created_at=datetime.now(JAKARTA_TZ),
            notes=data.get('notes', '') if data else ''
        )
        db.session.add(session)
        db.session.commit()
        return MeasurementSessionService._to_dict(session)

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all measurement sessions."""
        sessions = MeasurementSession.query.order_by(MeasurementSession.created_at.desc()).all()
        return [MeasurementSessionService._to_dict(s) for s in sessions]

    @staticmethod
    def get_by_id(session_id: str) -> Optional[Dict[str, Any]]:
        """Get a measurement session by ID."""
        session = MeasurementSession.query.get(session_id)
        return MeasurementSessionService._to_dict(session) if session else None

    @staticmethod
    def delete(session_id: str) -> bool:
        """Delete a measurement session and all related data (cascade delete)."""
        session = MeasurementSession.query.get(session_id)
        if not session:
            return False
        
        # Manually delete related records if CASCADE is not at database level
        # Delete all sensor readings for this session
        SensorReading.query.filter_by(session_id=session_id).delete()
        
        # Delete all stress history for this session
        HistoryStress.query.filter_by(session_id=session_id).delete()
        
        # Delete the session itself
        db.session.delete(session)
        db.session.commit()
        return True

    @staticmethod
    def _to_dict(session: MeasurementSession) -> Dict[str, Any]:
        """Convert MeasurementSession model to dictionary."""
        return {
            'id': session.id,
            'created_at': session.created_at.isoformat() if session.created_at else None,
            'notes': session.notes or ''
        }


class SensorReadingService:
    """Service class for handling sensor_readings CRUD operations."""

    @staticmethod
    def create(data: dict) -> Dict[str, Any]:
        """Create a new sensor reading."""
        reading = SensorReading(
            session_id=data['session_id'],
            timestamp=datetime.now(JAKARTA_TZ),
            hr=data['hr'],
            temp=data['temp'],
            eda=data['eda']
        )
        db.session.add(reading)
        db.session.commit()
        return SensorReadingService._to_dict(reading)

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all sensor readings."""
        readings = SensorReading.query.order_by(SensorReading.timestamp.desc()).all()
        return [SensorReadingService._to_dict(r) for r in readings]

    @staticmethod
    def get_by_id(reading_id: int) -> Optional[Dict[str, Any]]:
        """Get a sensor reading by ID."""
        reading = SensorReading.query.get(reading_id)
        return SensorReadingService._to_dict(reading) if reading else None

    @staticmethod
    def get_by_session(session_id: str) -> List[Dict[str, Any]]:
        """Get all sensor readings for a specific session."""
        readings = SensorReading.query.filter_by(session_id=session_id).order_by(SensorReading.timestamp.asc()).all()
        return [SensorReadingService._to_dict(r) for r in readings]

    @staticmethod
    def update(reading_id: int, data: dict) -> Optional[Dict[str, Any]]:
        """Update a sensor reading."""
        reading = SensorReading.query.get(reading_id)
        if not reading:
            return None

        if 'hr' in data:
            reading.hr = data['hr']
        if 'temp' in data:
            reading.temp = data['temp']
        if 'eda' in data:
            reading.eda = data['eda']
        if 'timestamp' in data:
            try:
                # Parse timestamp and convert to Jakarta timezone
                parsed_ts = datetime.fromisoformat(data['timestamp'])
                # If timezone-aware, convert to Jakarta; if naive, assume Jakarta
                if parsed_ts.tzinfo is not None:
                    reading.timestamp = parsed_ts.astimezone(JAKARTA_TZ)
                else:
                    reading.timestamp = parsed_ts.replace(tzinfo=JAKARTA_TZ)
            except Exception:
                pass

        db.session.commit()
        return SensorReadingService._to_dict(reading)

    @staticmethod
    def delete(reading_id: int) -> bool:
        """Delete a sensor reading."""
        reading = SensorReading.query.get(reading_id)
        if not reading:
            return False
        db.session.delete(reading)
        db.session.commit()
        return True

    @staticmethod
    def _to_dict(reading: SensorReading) -> Dict[str, Any]:
        """Convert SensorReading model to dictionary."""
        return {
            'id': reading.id,
            'session_id': reading.session_id,
            'timestamp': reading.timestamp.isoformat() if reading.timestamp else None,
            'hr': reading.hr,
            'temp': reading.temp,
            'eda': reading.eda,
            'created_at': reading.created_at.isoformat() if reading.created_at else None
        }


class UserService:
    """Service class for handling user authentication and CRUD operations."""

    @staticmethod
    def create_user(username: str, email: str, password: str) -> Dict[str, Any]:
        """Create a new user with hashed password."""
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            raise ValueError("Username already exists")
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already exists")
        
        # Create new user
        user = User(
            username=username,
            email=email
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user.to_dict()

    @staticmethod
    def authenticate(username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return user data with tokens if successful."""
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return None
        
        # Create JWT tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        user = User.query.get(user_id)
        return user.to_dict() if user else None

    @staticmethod
    def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
        """Get user by username."""
        user = User.query.filter_by(username=username).first()
        return user.to_dict() if user else None

    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        user = User.query.filter_by(email=email).first()
        return user.to_dict() if user else None

    @staticmethod
    def get_all_users() -> List[Dict[str, Any]]:
        """Get all users."""
        users = User.query.all()
        return [user.to_dict() for user in users]

    @staticmethod
    def update_user(user_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user information."""
        user = User.query.get(user_id)
        if not user:
            return None
        
        # Update username if provided and not duplicate
        if 'username' in data and data['username'] != user.username:
            if User.query.filter_by(username=data['username']).first():
                raise ValueError("Username already exists")
            user.username = data['username']
        
        # Update email if provided and not duplicate
        if 'email' in data and data['email'] != user.email:
            if User.query.filter_by(email=data['email']).first():
                raise ValueError("Email already exists")
            user.email = data['email']
        
        # Update password if provided
        if 'password' in data:
            user.set_password(data['password'])
        
        user.updated_at = datetime.now(JAKARTA_TZ)
        db.session.commit()
        
        return user.to_dict()

    @staticmethod
    def delete_user(user_id: str) -> bool:
        """Delete a user."""
        user = User.query.get(user_id)
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()
        return True

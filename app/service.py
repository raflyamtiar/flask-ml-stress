from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
from . import db
from .models import AppInfo, HistoryStress
import os
from pathlib import Path
import joblib
import pandas as pd

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
    def create(data: dict):
        # Use Jakarta time for timestamp
        ts_val = datetime.now(JAKARTA_TZ)

        rec = HistoryStress(
            timestamp=ts_val,
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
                rec.timestamp = datetime.fromisoformat(data['timestamp'])
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
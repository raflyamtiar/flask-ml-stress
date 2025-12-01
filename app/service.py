from datetime import datetime
from typing import Optional, List, Dict, Any
from . import db
from .models import AppInfo


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
        
        app_info.updated_at = datetime.utcnow()
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
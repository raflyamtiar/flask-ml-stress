"""
Test script to verify:
1. JWT authentication on protected endpoints
2. Cascade delete from stress_history to session
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from app.models import MeasurementSession, SensorReading, HistoryStress, User
from app.service import MeasurementSessionService, SensorReadingService, StressHistoryService, UserService
from datetime import datetime, timezone, timedelta
from flask_jwt_extended import create_access_token

JAKARTA_TZ = timezone(timedelta(hours=7))

def test_jwt_protected_endpoints():
    """Test that protected endpoints require JWT"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("JWT AUTHENTICATION TEST")
        print("=" * 60)
        
        # Create test client
        client = app.test_client()
        
        # Test endpoints that should require authentication
        protected_endpoints = [
            ('PUT', '/api/app-info/1', {'app_name': 'Test'}),
            ('DELETE', '/api/app-info/1', None),
            ('DELETE', '/api/sessions/test-uuid', None),
            ('PUT', '/api/sensor-readings/1', {'hr': 75.0}),
            ('DELETE', '/api/sensor-readings/1', None),
        ]
        
        print("\n1. Testing protected endpoints WITHOUT JWT token...")
        for method, endpoint, data in protected_endpoints:
            if method == 'PUT':
                response = client.put(endpoint, json=data)
            elif method == 'DELETE':
                response = client.delete(endpoint)
            
            status = "✓ PROTECTED" if response.status_code == 401 else f"❌ NOT PROTECTED (status: {response.status_code})"
            print(f"   {method} {endpoint}: {status}")
        
        print("\n" + "=" * 60)


def test_cascade_delete_stress_to_session():
    """Test cascade delete from stress_history to session"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("STRESS_HISTORY → SESSION CASCADE DELETE TEST")
        print("=" * 60)
        
        # 1. Create a test session
        print("\n1. Creating test session...")
        session_data = MeasurementSessionService.create({'notes': 'Test cascade from stress to session'})
        session_id = session_data['id']
        print(f"   ✓ Created session: {session_id}")
        
        # 2. Add multiple sensor readings to this session
        print("\n2. Adding sensor readings...")
        for i in range(3):
            reading_data = {
                'session_id': session_id,
                'timestamp': datetime.now(JAKARTA_TZ),
                'hr': 75.0 + i,
                'temp': 36.5 + i * 0.1,
                'eda': 0.5 + i * 0.05
            }
            SensorReadingService.create(reading_data)
        print(f"   ✓ Added 3 sensor readings")
        
        # 3. Add multiple stress history records to this session
        print("\n3. Adding stress history records...")
        stress_ids = []
        for i in range(3):
            history_data = {
                'session_id': session_id,
                'timestamp': datetime.now(JAKARTA_TZ),
                'hr': 75.0 + i,
                'temp': 36.5 + i * 0.1,
                'eda': 0.5 + i * 0.05,
                'label': 'Normal',
                'confidence_level': 0.95
            }
            result = StressHistoryService.create(history_data)
            stress_ids.append(result['id'])
        print(f"   ✓ Added 3 stress history records: {stress_ids}")
        
        # 4. Count BEFORE delete
        print("\n4. Counting records BEFORE delete...")
        sensor_count_before = SensorReading.query.filter_by(session_id=session_id).count()
        history_count_before = HistoryStress.query.filter_by(session_id=session_id).count()
        session_exists_before = MeasurementSession.query.filter_by(id=session_id).first() is not None
        print(f"   Sessions: {1 if session_exists_before else 0}")
        print(f"   Sensor readings: {sensor_count_before}")
        print(f"   Stress history: {history_count_before}")
        
        # 5. Delete ONE stress history record
        print(f"\n5. Deleting ONE stress history record (ID: {stress_ids[0]})...")
        print("   ⚠️  This should cascade delete the entire session!")
        result = StressHistoryService.delete(stress_ids[0])
        print(f"   Delete result: {result}")
        
        # 6. Count AFTER delete
        print("\n6. Counting records AFTER delete...")
        sensor_count_after = SensorReading.query.filter_by(session_id=session_id).count()
        history_count_after = HistoryStress.query.filter_by(session_id=session_id).count()
        session_exists_after = MeasurementSession.query.filter_by(id=session_id).first() is not None
        print(f"   Sessions: {1 if session_exists_after else 0}")
        print(f"   Sensor readings: {sensor_count_after}")
        print(f"   Stress history: {history_count_after}")
        
        # 7. Verify cascade delete worked
        print("\n" + "=" * 60)
        print("RESULTS:")
        print("=" * 60)
        
        if sensor_count_after == 0 and history_count_after == 0 and not session_exists_after:
            print("✅ CASCADE DELETE FROM STRESS_HISTORY → SESSION WORKS!")
            print("   Deleting one stress history record removed:")
            print(f"   - The session (1 session)")
            print(f"   - All sensor readings ({sensor_count_before} readings)")
            print(f"   - All stress history records ({history_count_before} records)")
        else:
            print("❌ CASCADE DELETE FAILED!")
            if session_exists_after:
                print("   Session still exists")
            if sensor_count_after > 0:
                print(f"   {sensor_count_after} sensor readings still exist")
            if history_count_after > 0:
                print(f"   {history_count_after} stress history records still exist")
        
        print("=" * 60)


if __name__ == '__main__':
    test_jwt_protected_endpoints()
    print("\n\n")
    test_cascade_delete_stress_to_session()

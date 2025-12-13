"""
Test script to verify cascade delete functionality
When a session is deleted, all related stress_history and sensor_readings should be deleted too
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from app.models import MeasurementSession, SensorReading, HistoryStress
from app.service import MeasurementSessionService, SensorReadingService, StressHistoryService
from datetime import datetime, timezone, timedelta
import uuid

JAKARTA_TZ = timezone(timedelta(hours=7))

def test_cascade_delete():
    """Test cascade delete functionality"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("CASCADE DELETE TEST")
        print("=" * 60)
        
        # 1. Create a test session
        print("\n1. Creating test session...")
        session_data = MeasurementSessionService.create({'notes': 'Test cascade delete'})
        session_id = session_data['id']
        print(f"   ✓ Created session: {session_id}")
        
        # 2. Add sensor readings to this session
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
        
        # 3. Add stress history to this session
        print("\n3. Adding stress history...")
        for i in range(2):
            history_data = {
                'session_id': session_id,
                'timestamp': datetime.now(JAKARTA_TZ),
                'hr': 75.0 + i,
                'temp': 36.5 + i * 0.1,
                'eda': 0.5 + i * 0.05,
                'label': 'Normal',
                'confidence_level': 0.95
            }
            StressHistoryService.create(history_data)
        print(f"   ✓ Added 2 stress history records")
        
        # 4. Count related records BEFORE delete
        print("\n4. Counting records BEFORE delete...")
        sensor_count_before = SensorReading.query.filter_by(session_id=session_id).count()
        history_count_before = HistoryStress.query.filter_by(session_id=session_id).count()
        print(f"   Sensor readings: {sensor_count_before}")
        print(f"   Stress history: {history_count_before}")
        
        # 5. Delete the session
        print(f"\n5. Deleting session {session_id}...")
        result = MeasurementSessionService.delete(session_id)
        print(f"   Delete result: {result}")
        
        # 6. Count related records AFTER delete
        print("\n6. Counting records AFTER delete...")
        sensor_count_after = SensorReading.query.filter_by(session_id=session_id).count()
        history_count_after = HistoryStress.query.filter_by(session_id=session_id).count()
        session_exists = MeasurementSession.query.get(session_id) is not None
        print(f"   Sensor readings: {sensor_count_after}")
        print(f"   Stress history: {history_count_after}")
        print(f"   Session exists: {session_exists}")
        
        # 7. Verify cascade delete worked
        print("\n" + "=" * 60)
        print("RESULTS:")
        print("=" * 60)
        
        if sensor_count_after == 0 and history_count_after == 0 and not session_exists:
            print("✅ CASCADE DELETE WORKS CORRECTLY!")
            print("   All related data was deleted when session was removed.")
        else:
            print("❌ CASCADE DELETE FAILED!")
            if sensor_count_after > 0:
                print(f"   {sensor_count_after} sensor readings still exist (orphaned)")
            if history_count_after > 0:
                print(f"   {history_count_after} stress history records still exist (orphaned)")
            if session_exists:
                print("   Session still exists (delete failed)")
        
        print("=" * 60)

if __name__ == '__main__':
    test_cascade_delete()

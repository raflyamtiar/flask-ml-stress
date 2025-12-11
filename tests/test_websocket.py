"""
WebSocket Test Script for ESP32 Simulation
Test real-time sensor data sending via Socket.IO
"""

import socketio
import time
import random
from datetime import datetime, timezone, timedelta

# Jakarta timezone (UTC+7)
JAKARTA_TZ = timezone(timedelta(hours=7))

# Create Socket.IO client
sio = socketio.Client()

# Event handlers
@sio.on('connect')
def on_connect():
    print('✓ Connected to WebSocket server')
    print(f'  Connection ID: {sio.sid}')

@sio.on('disconnect')
def on_disconnect():
    print('✗ Disconnected from server')

@sio.on('connection_status')
def on_connection_status(data):
    print(f'📋 Connection Status: {data}')

@sio.on('data_received')
def on_data_received(data):
    print(f'✓ Server Response:')
    print(f'  Status: {data.get("status")}')
    print(f'  Message: {data.get("message")}')
    print(f'  Record ID: {data.get("record_id")}')
    if 'stress_prediction' in data:
        pred = data['stress_prediction']
        print(f'  Stress Level: {pred.get("label")}')
        print(f'  Confidence: {pred.get("confidence"):.2f}')

@sio.on('error')
def on_error(error):
    print(f'✗ Error: {error}')

@sio.on('pong')
def on_pong(data):
    print(f'🏓 Pong received: {data}')


def generate_sensor_data(stress_level='normal'):
    """Generate realistic sensor data based on stress level"""
    
    if stress_level == 'normal':
        hr = random.uniform(60, 80)
        temp = random.uniform(36.0, 36.8)
        eda = random.uniform(0.3, 0.5)
    elif stress_level == 'medium':
        hr = random.uniform(80, 95)
        temp = random.uniform(36.8, 37.2)
        eda = random.uniform(0.5, 0.7)
    else:  # high stress
        hr = random.uniform(95, 120)
        temp = random.uniform(37.2, 38.0)
        eda = random.uniform(0.7, 1.0)
    
    return {
        'hr': round(hr, 1),
        'temp': round(temp, 1),
        'eda': round(eda, 2),
        'device_id': 'ESP32_PYTHON_TEST',
        'timestamp': datetime.now(JAKARTA_TZ).isoformat()
    }


def test_single_send():
    """Test sending a single sensor reading"""
    print('\n' + '='*60)
    print('TEST 1: Single Sensor Data Transmission')
    print('='*60)
    
    try:
        # Connect as ESP32
        sio.connect('http://127.0.0.1:5000', 
                    transports=['websocket'],
                    wait_timeout=10)
        
        # Generate and send data
        sensor_data = generate_sensor_data('normal')
        print(f'\n📤 Sending sensor data:')
        print(f'   HR: {sensor_data["hr"]} BPM')
        print(f'   Temp: {sensor_data["temp"]}°C')
        print(f'   EDA: {sensor_data["eda"]}')
        
        sio.emit('esp32_sensor_data', sensor_data)
        
        # Wait for response
        time.sleep(2)
        
        sio.disconnect()
        print('\n✓ Test completed successfully\n')
        
    except Exception as e:
        print(f'\n✗ Test failed: {e}\n')


def test_multiple_sends():
    """Test sending multiple sensor readings with varying stress levels"""
    print('\n' + '='*60)
    print('TEST 2: Multiple Data Transmissions (5 readings)')
    print('='*60)
    
    try:
        # Connect as ESP32
        sio.connect('http://127.0.0.1:5000', 
                    transports=['websocket'],
                    wait_timeout=10)
        
        stress_levels = ['normal', 'normal', 'medium', 'high', 'normal']
        
        for i, level in enumerate(stress_levels, 1):
            sensor_data = generate_sensor_data(level)
            
            print(f'\n📤 Sending reading #{i} ({level} stress):')
            print(f'   HR: {sensor_data["hr"]} BPM')
            print(f'   Temp: {sensor_data["temp"]}°C')
            print(f'   EDA: {sensor_data["eda"]}')
            
            sio.emit('esp32_sensor_data', sensor_data)
            time.sleep(1.5)
        
        # Wait for final response
        time.sleep(2)
        
        sio.disconnect()
        print('\n✓ Test completed successfully\n')
        
    except Exception as e:
        print(f'\n✗ Test failed: {e}\n')


def test_ping():
    """Test ping-pong connection"""
    print('\n' + '='*60)
    print('TEST 3: Ping-Pong Connection Test')
    print('='*60)
    
    try:
        sio.connect('http://127.0.0.1:5000', 
                    transports=['websocket'],
                    wait_timeout=10)
        
        print('\n🏓 Sending ping...')
        sio.emit('ping')
        
        time.sleep(2)
        
        sio.disconnect()
        print('\n✓ Test completed successfully\n')
        
    except Exception as e:
        print(f'\n✗ Test failed: {e}\n')


def test_continuous_monitoring(duration=15):
    """Simulate continuous monitoring for specified duration"""
    print('\n' + '='*60)
    print(f'TEST 4: Continuous Monitoring ({duration} seconds)')
    print('='*60)
    
    try:
        sio.connect('http://127.0.0.1:5000', 
                    transports=['websocket'],
                    wait_timeout=10)
        
        print(f'\n🔄 Sending data every 3 seconds for {duration} seconds...\n')
        
        start_time = time.time()
        count = 0
        
        while (time.time() - start_time) < duration:
            count += 1
            # Randomly vary stress level
            level = random.choice(['normal', 'normal', 'medium', 'high'])
            sensor_data = generate_sensor_data(level)
            
            print(f'📤 Reading #{count} - HR:{sensor_data["hr"]} Temp:{sensor_data["temp"]} EDA:{sensor_data["eda"]}')
            
            sio.emit('esp32_sensor_data', sensor_data)
            time.sleep(3)
        
        sio.disconnect()
        print(f'\n✓ Sent {count} readings successfully\n')
        
    except Exception as e:
        print(f'\n✗ Test failed: {e}\n')


if __name__ == '__main__':
    print('\n' + '='*60)
    print('🔌 WebSocket ESP32 Simulator')
    print('='*60)
    print('Make sure Flask server is running on http://127.0.0.1:5000')
    print('='*60 + '\n')
    
    input('Press Enter to start tests...')
    
    # Run tests
    test_single_send()
    time.sleep(1)
    
    test_ping()
    time.sleep(1)
    
    test_multiple_sends()
    time.sleep(1)
    
    # Ask for continuous monitoring
    response = input('Run continuous monitoring test? (y/n): ')
    if response.lower() == 'y':
        duration = input('Duration in seconds (default 15): ')
        try:
            duration = int(duration) if duration else 15
        except:
            duration = 15
        test_continuous_monitoring(duration)
    
    print('\n' + '='*60)
    print('✓ All tests completed!')
    print('='*60 + '\n')

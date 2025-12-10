"""
WebSocket Event Handlers for ESP32 and React Frontend Communication

This module handles:
- Real-time data relay from ESP32 to React frontend
- No database persistence or ML predictions
"""

from flask import request
from flask_socketio import emit, join_room, leave_room, disconnect
from datetime import datetime
import logging

from . import socketio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store connected clients info
connected_clients = {}


@socketio.on('connect')
def handle_connect(auth=None):
    """Handle client connection."""
    client_id = request.sid
    client_type = request.args.get('type', 'unknown')  # 'esp32', 'frontend', or 'unknown'
    
    connected_clients[client_id] = {
        'type': client_type,
        'connected_at': datetime.now(),
        'last_seen': datetime.now()
    }
    
    logger.info(f"Client connected: {client_id} (type: {client_type})")
    
    # Join appropriate room based on client type
    if client_type == 'frontend':
        join_room('frontend_clients')
        emit('connection_status', {'status': 'connected', 'message': 'Connected to stress monitoring server'})
    elif client_type == 'esp32':
        join_room('esp32_clients')
        emit('connection_status', {'status': 'connected', 'message': 'ESP32 connected successfully'})
    
    # Broadcast client count to frontend
    frontend_count = sum(1 for c in connected_clients.values() if c['type'] == 'frontend')
    esp32_count = sum(1 for c in connected_clients.values() if c['type'] == 'esp32')
    
    socketio.emit('client_stats', {
        'frontend_clients': frontend_count,
        'esp32_clients': esp32_count,
        'total_clients': len(connected_clients)
    }, room='frontend_clients')


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    client_id = request.sid
    
    if client_id in connected_clients:
        client_info = connected_clients[client_id]
        logger.info(f"Client disconnected: {client_id} (type: {client_info['type']})")
        del connected_clients[client_id]
        
        # Update client count for frontend
        frontend_count = sum(1 for c in connected_clients.values() if c['type'] == 'frontend')
        esp32_count = sum(1 for c in connected_clients.values() if c['type'] == 'esp32')
        
        socketio.emit('client_stats', {
            'frontend_clients': frontend_count,
            'esp32_clients': esp32_count,
            'total_clients': len(connected_clients)
        }, room='frontend_clients')


@socketio.on('esp32_live_data')
def handle_esp32_live_data(data):
    """
    Handle real-time ESP32 data relay without database or ML processing.
    
    Expected data format:
    {
        'timestamp': '2024-12-10T10:30:00Z',  # ISO format or Unix timestamp (optional)
        'hr': 75.5,        # Heart Rate
        'temp': 36.2,      # Temperature in Celsius
        'eda': 0.45,       # Electrodermal Activity
        'device_id': 'ESP32_001'  # Optional device identifier
    }
    """
    try:
        client_id = request.sid

        # Validate client type
        if client_id not in connected_clients or connected_clients[client_id]['type'] != 'esp32':
            logger.warning(f"Unauthorized live data from {client_id}")
            emit('error', {'message': 'Unauthorized: Only ESP32 clients can send live data'})
            return

        # Update last seen
        connected_clients[client_id]['last_seen'] = datetime.now()

        # Validate required fields
        required_fields = ['hr', 'temp', 'eda']
        if not all(field in data for field in required_fields):
            emit('error', {'message': f'Missing required fields: {required_fields}'})
            return

        # Parse timestamp if provided
        timestamp = data.get('timestamp')
        if timestamp:
            try:
                if isinstance(timestamp, (int, float)):
                    timestamp = datetime.fromtimestamp(timestamp)
                elif isinstance(timestamp, str):
                    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except (ValueError, TypeError):
                timestamp = datetime.now()
        else:
            timestamp = datetime.now()

        # Extract sensor values
        hr = float(data['hr'])
        temp = float(data['temp'])
        eda = float(data['eda'])
        device_id = data.get('device_id', 'ESP32_Unknown')

        # Prepare relay payload (no ML, no DB)
        relay_payload = {
            'timestamp': timestamp.isoformat(),
            'hr': hr,
            'temp': temp,
            'eda': eda,
            'device_id': device_id
        }

        # Send confirmation to ESP32
        emit('live_data_received', {
            'status': 'success',
            'message': 'Live data relayed successfully'
        })

        # Broadcast to all frontend clients
        socketio.emit('live_sensor_data', relay_payload, room='frontend_clients')
        
        logger.info(f"Relayed live data from {device_id}: HR={hr}, Temp={temp}, EDA={eda}")

    except Exception as e:
        logger.error(f"Error relaying ESP32 live data: {e}")
        emit('error', {'message': f'Live data relay error: {str(e)}'})


@socketio.on('ping')
def handle_ping():
    """Handle ping from clients for connection testing."""
    client_id = request.sid
    if client_id in connected_clients:
        connected_clients[client_id]['last_seen'] = datetime.now()
    
    emit('pong', {'timestamp': datetime.now().isoformat()})


# Health check endpoint for WebSocket
@socketio.on('health_check')
def handle_health_check():
    """Handle health check requests."""
    emit('health_status', {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'connected_clients': len(connected_clients),
        'server_info': 'Flask-SocketIO Real-time Relay Server'
    })

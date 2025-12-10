"""
WebSocket Event Handlers for ESP32 and React Frontend Communication

This module handles:
- ESP32 sensor data ingestion via WebSocket
- Real-time data broadcasting to React frontend
- Stress level analysis and notifications
"""

from flask import request
from flask_socketio import emit, join_room, leave_room, disconnect
from datetime import datetime
import json
import logging

from . import socketio, db
from .models import HistoryStress
from .service import StressModelService

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


@socketio.on('esp32_sensor_data')
def handle_esp32_data(data):
    """
    Handle sensor data from ESP32.
    
    Expected data format:
    {
        'timestamp': '2024-12-10T10:30:00Z',  # ISO format or Unix timestamp
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
            logger.warning(f"Unauthorized sensor data from {client_id}")
            emit('error', {'message': 'Unauthorized: Only ESP32 clients can send sensor data'})
            return
        
        # Update last seen
        connected_clients[client_id]['last_seen'] = datetime.now()
        
        # Validate required fields
        required_fields = ['hr', 'temp', 'eda']
        if not all(field in data for field in required_fields):
            emit('error', {'message': f'Missing required fields: {required_fields}'})
            return
        
        # Parse timestamp
        timestamp = data.get('timestamp')
        if timestamp:
            try:
                if isinstance(timestamp, (int, float)):
                    # Unix timestamp
                    timestamp = datetime.fromtimestamp(timestamp)
                elif isinstance(timestamp, str):
                    # ISO format
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
        
        # Perform stress analysis using ML model
        try:
            prediction_result = StressModelService.predict_stress({
                'hr': hr,
                'temp': temp,
                'eda': eda
            })
            
            stress_label = prediction_result.get('prediction', 'unknown')
            confidence = prediction_result.get('confidence', 0.0)
            
        except Exception as e:
            logger.error(f"Stress prediction error: {e}")
            stress_label = 'error'
            confidence = 0.0
        
        # Save to database
        history_record = HistoryStress(
            timestamp=timestamp,
            hr=hr,
            temp=temp,
            eda=eda,
            label=stress_label,
            confidence_level=confidence,
            notes=f"Data from {device_id}"
        )
        
        try:
            db.session.add(history_record)
            db.session.commit()
            logger.info(f"Saved sensor data from {device_id}: HR={hr}, Temp={temp}, EDA={eda}, Stress={stress_label}")
        except Exception as e:
            logger.error(f"Database error: {e}")
            db.session.rollback()
            emit('error', {'message': 'Failed to save data to database'})
            return
        
        # Prepare data for real-time broadcast
        real_time_data = {
            'id': history_record.id,
            'timestamp': timestamp.isoformat(),
            'hr': hr,
            'temp': temp,
            'eda': eda,
            'stress_level': stress_label,
            'confidence': round(confidence * 100, 2),  # Convert to percentage
            'device_id': device_id,
            'created_at': history_record.created_at.isoformat()
        }
        
        # Send confirmation to ESP32
        emit('data_received', {
            'status': 'success',
            'message': 'Data processed successfully',
            'record_id': history_record.id,
            'stress_prediction': {
                'label': stress_label,
                'confidence': confidence
            }
        })
        
        # Broadcast to all frontend clients
        socketio.emit('new_sensor_data', real_time_data, room='frontend_clients')
        
        # Send alert if high stress detected
        if stress_label in ['high_stress', 'very_high_stress'] and confidence > 0.7:
            alert_data = {
                'type': 'stress_alert',
                'level': stress_label,
                'confidence': round(confidence * 100, 2),
                'timestamp': timestamp.isoformat(),
                'message': f"High stress level detected with {round(confidence * 100, 1)}% confidence",
                'sensor_data': {
                    'hr': hr,
                    'temp': temp,
                    'eda': eda
                }
            }
            socketio.emit('stress_alert', alert_data, room='frontend_clients')
            logger.warning(f"Stress alert sent: {stress_label} ({confidence:.2%})")
        
    except Exception as e:
        logger.error(f"Error processing ESP32 data: {e}")
        emit('error', {'message': f'Data processing error: {str(e)}'})


@socketio.on('frontend_request_history')
def handle_history_request(data):
    """
    Handle frontend request for historical data.
    
    Expected data format:
    {
        'limit': 100,           # Number of recent records
        'start_date': '2024-12-01',  # Optional start date
        'end_date': '2024-12-10'     # Optional end date
    }
    """
    try:
        client_id = request.sid
        
        # Validate client type
        if client_id not in connected_clients or connected_clients[client_id]['type'] != 'frontend':
            emit('error', {'message': 'Unauthorized: Only frontend clients can request history'})
            return
        
        limit = data.get('limit', 100)
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        # Build query
        query = HistoryStress.query.order_by(HistoryStress.timestamp.desc())
        
        if start_date:
            try:
                start_date = datetime.fromisoformat(start_date)
                query = query.filter(HistoryStress.timestamp >= start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.fromisoformat(end_date)
                query = query.filter(HistoryStress.timestamp <= end_date)
            except ValueError:
                pass
        
        records = query.limit(limit).all()
        
        # Format data for frontend
        history_data = []
        for record in records:
            history_data.append({
                'id': record.id,
                'timestamp': record.timestamp.isoformat(),
                'hr': record.hr,
                'temp': record.temp,
                'eda': record.eda,
                'stress_level': record.label,
                'confidence': round((record.confidence_level or 0) * 100, 2),
                'notes': record.notes,
                'created_at': record.created_at.isoformat()
            })
        
        emit('history_data', {
            'status': 'success',
            'data': history_data,
            'count': len(history_data),
            'request_params': {
                'limit': limit,
                'start_date': start_date.isoformat() if start_date else None,
                'end_date': end_date.isoformat() if end_date else None
            }
        })
        
        logger.info(f"Sent {len(history_data)} historical records to frontend client {client_id}")
        
    except Exception as e:
        logger.error(f"Error processing history request: {e}")
        emit('error', {'message': f'History request error: {str(e)}'})


@socketio.on('ping')
def handle_ping():
    """Handle ping from clients for connection testing."""
    client_id = request.sid
    if client_id in connected_clients:
        connected_clients[client_id]['last_seen'] = datetime.now()
    
    emit('pong', {'timestamp': datetime.now().isoformat()})


@socketio.on('frontend_subscribe_alerts')
def handle_alert_subscription(data):
    """Handle frontend subscription to stress alerts."""
    try:
        client_id = request.sid
        
        if client_id not in connected_clients or connected_clients[client_id]['type'] != 'frontend':
            emit('error', {'message': 'Unauthorized: Only frontend clients can subscribe to alerts'})
            return
        
        # Join alert room
        join_room('alert_subscribers')
        
        # Send confirmation
        emit('subscription_status', {
            'status': 'subscribed',
            'message': 'Successfully subscribed to stress alerts'
        })
        
        logger.info(f"Frontend client {client_id} subscribed to alerts")
        
    except Exception as e:
        logger.error(f"Error handling alert subscription: {e}")
        emit('error', {'message': f'Subscription error: {str(e)}'})


@socketio.on('error_default')
def default_error_handler(e):
    """Handle uncaught SocketIO errors."""
    logger.error(f"SocketIO error: {e}")
    emit('error', {'message': 'An unexpected error occurred'})


# Health check endpoint for WebSocket
@socketio.on('health_check')
def handle_health_check():
    """Handle health check requests."""
    emit('health_status', {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'connected_clients': len(connected_clients),
        'server_info': 'Flask-SocketIO Stress Monitoring Server'
    })

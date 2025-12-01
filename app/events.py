"""
WebSocket event handlers for Flask-SocketIO.

Architecture:
    IoT (ESP32) → Flask (WebSocket Server) → React (WebSocket Client)

Namespaces:
    /ws/esp32  - ESP32 connects here and sends sensor data
    /ws/react  - React connects here and receives sensor updates
"""

from flask_socketio import emit, Namespace
from datetime import datetime


# Store connected clients info (optional, for debugging/monitoring)
connected_clients = {
    'esp32': set(),
    'react': set()
}


class ESP32Namespace(Namespace):
    """
    Namespace for ESP32 IoT device connections.
    ESP32 sends sensor data via 'message' event.
    """

    def on_connect(self):
        """Handle ESP32 client connection."""
        from flask import request
        client_id = request.sid
        connected_clients['esp32'].add(client_id)
        print(f"[ESP32] Client connected: {client_id}")
        print(f"[ESP32] Total connected: {len(connected_clients['esp32'])}")

    def on_disconnect(self):
        """Handle ESP32 client disconnection."""
        from flask import request
        client_id = request.sid
        connected_clients['esp32'].discard(client_id)
        print(f"[ESP32] Client disconnected: {client_id}")
        print(f"[ESP32] Total connected: {len(connected_clients['esp32'])}")

    def on_message(self, data):
        """
        Handle incoming sensor data from ESP32.
        
        Expected data format:
            {"temp": 30.5, "hum": 65.1}
        
        This will be broadcast to all React clients via 'sensor_update' event.
        """
        from flask import request
        client_id = request.sid
        
        print(f"[ESP32] Received data from {client_id}: {data}")
        
        # Validate data
        if not isinstance(data, dict):
            print(f"[ESP32] Invalid data format (expected dict): {data}")
            return
        
        # Add timestamp to the data
        sensor_data = {
            'temp': data.get('temp'),
            'hum': data.get('hum'),
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'esp32'
        }
        
        # Broadcast to all React clients
        emit('sensor_update', sensor_data, namespace='/ws/react', broadcast=True)
        print(f"[ESP32] Broadcasted to React clients: {sensor_data}")


class ReactNamespace(Namespace):
    """
    Namespace for React frontend connections.
    React receives sensor updates via 'sensor_update' event.
    """

    def on_connect(self):
        """Handle React client connection."""
        from flask import request
        client_id = request.sid
        connected_clients['react'].add(client_id)
        print(f"[React] Client connected: {client_id}")
        print(f"[React] Total connected: {len(connected_clients['react'])}")
        
        # Send welcome message to the newly connected React client
        emit('connection_status', {
            'status': 'connected',
            'message': 'Successfully connected to WebSocket server',
            'timestamp': datetime.utcnow().isoformat()
        })

    def on_disconnect(self):
        """Handle React client disconnection."""
        from flask import request
        client_id = request.sid
        connected_clients['react'].discard(client_id)
        print(f"[React] Client disconnected: {client_id}")
        print(f"[React] Total connected: {len(connected_clients['react'])}")


def init_socket_events(socketio):
    """
    Initialize all WebSocket event handlers.
    
    This function registers the namespace handlers with the SocketIO instance.
    Called from create_app() in app/__init__.py.
    
    Args:
        socketio: The Flask-SocketIO instance
    """
    # Register namespaces
    socketio.on_namespace(ESP32Namespace('/ws/esp32'))
    socketio.on_namespace(ReactNamespace('/ws/react'))
    
    print("[SocketIO] Event handlers initialized")
    print("[SocketIO] Namespaces registered: /ws/esp32, /ws/react")


# Utility function to broadcast sensor data from anywhere in the app
def broadcast_to_react(socketio, data):
    """
    Utility function to broadcast data to all React clients.
    
    Args:
        socketio: The Flask-SocketIO instance
        data: Dictionary containing the data to broadcast
    
    Usage:
        from app import socketio
        from app.events import broadcast_to_react
        broadcast_to_react(socketio, {'temp': 30.5, 'hum': 65.1})
    """
    sensor_data = {
        **data,
        'timestamp': datetime.utcnow().isoformat()
    }
    socketio.emit('sensor_update', sensor_data, namespace='/ws/react')

from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
	# Use socketio.run() instead of app.run() for WebSocket support
	# This enables Flask-SocketIO with eventlet async mode
	print("Starting Flask-SocketIO server...")
	print("WebSocket namespaces available:")
	print("  - ESP32:  ws://0.0.0.0:5000/ws/esp32")
	print("  - React:  ws://0.0.0.0:5000/ws/react")
	print("-" * 50)
	socketio.run(app, host='0.0.0.0', port=5000, debug=True)

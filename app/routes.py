from flask import Blueprint, render_template, request, jsonify
from .service import AppInfoService, StressHistoryService, StressModelService
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')

# RESTful API endpoints for app_info CRUD

@main.route('/api/app-info', methods=['GET'])
def get_app_infos():
	"""Get all app info records."""
	try:
		app_infos = AppInfoService.get_all()
		return jsonify({
			'success': True,
			'data': app_infos
		})
	except Exception as e:
		return jsonify({
			'success': False,
			'error': str(e)
		}), 500

@main.route('/api/app-info/<int:app_id>', methods=['GET'])
def get_app_info(app_id):
	"""Get a specific app info record by ID."""
	try:
		app_info = AppInfoService.get_by_id(app_id)
		if app_info:
			return jsonify({
				'success': True,
				'data': app_info
			})
		else:
			return jsonify({
				'success': False,
				'error': 'App info not found'
			}), 404
	except Exception as e:
		return jsonify({
			'success': False,
			'error': str(e)
		}), 500

@main.route('/api/app-info', methods=['POST'])
def create_app_info():
	"""Create a new app info record."""
	try:
		data = request.get_json()
		if not data or 'app_name' not in data:
			return jsonify({
				'success': False,
				'error': 'app_name is required'
			}), 400
		
		app_info = AppInfoService.create(data)
		return jsonify({
			'success': True,
			'data': app_info
		}), 201
	except Exception as e:
		return jsonify({
			'success': False,
			'error': str(e)
		}), 500

@main.route('/api/app-info/<int:app_id>', methods=['PUT'])
def update_app_info(app_id):
	"""Update an existing app info record."""
	try:
		data = request.get_json()
		if not data:
			return jsonify({
				'success': False,
				'error': 'No data provided'
			}), 400
		
		app_info = AppInfoService.update(app_id, data)
		if app_info:
			return jsonify({
				'success': True,
				'data': app_info
			})
		else:
			return jsonify({
				'success': False,
				'error': 'App info not found'
			}), 404
	except Exception as e:
		return jsonify({
			'success': False,
			'error': str(e)
		}), 500

@main.route('/api/app-info/<int:app_id>', methods=['DELETE'])
def delete_app_info(app_id):
	"""Delete an app info record."""
	try:
		success = AppInfoService.delete(app_id)
		if success:
			return jsonify({
				'success': True,
				'message': 'App info deleted successfully'
			})
		else:
			return jsonify({
				'success': False,
				'error': 'App info not found'
			}), 404
	except Exception as e:
		return jsonify({
			'success': False,
			'error': str(e)
		}), 500


@main.route('/api', methods=['GET'])
def api_status():
	"""Simple API status endpoint."""
	try:
		return jsonify({
			'success': True,
			'status': 'ok',
			'message': 'API is running'
		})
	except Exception as e:
		return jsonify({
			'success': False,
			'error': str(e)
		}), 500


# RESTful API endpoints for stress_history CRUD

@main.route('/api/stress-history', methods=['GET'])
def get_stress_histories():
	try:
		items = StressHistoryService.get_all()
		return jsonify({'success': True, 'data': items})
	except Exception as e:
		return jsonify({'success': False, 'error': str(e)}), 500


@main.route('/api/stress-history/<int:rec_id>', methods=['GET'])
def get_stress_history(rec_id):
	try:
		item = StressHistoryService.get_by_id(rec_id)
		if item:
			return jsonify({'success': True, 'data': item})
		return jsonify({'success': False, 'error': 'Record not found'}), 404
	except Exception as e:
		return jsonify({'success': False, 'error': str(e)}), 500


@main.route('/api/stress-history', methods=['POST'])
def create_stress_history():
	try:
		data = request.get_json() or {}
		# timestamp is optional; service will set if missing/invalid
		item = StressHistoryService.create(data)
		return jsonify({'success': True, 'data': item}), 201
	except Exception as e:
		return jsonify({'success': False, 'error': str(e)}), 500


@main.route('/api/stress-history/<int:rec_id>', methods=['PUT'])
def update_stress_history(rec_id):
	try:
		data = request.get_json() or {}
		item = StressHistoryService.update(rec_id, data)
		if item:
			return jsonify({'success': True, 'data': item})
		return jsonify({'success': False, 'error': 'Record not found'}), 404
	except Exception as e:
		return jsonify({'success': False, 'error': str(e)}), 500


@main.route('/api/stress-history/<int:rec_id>', methods=['DELETE'])
def delete_stress_history(rec_id):
	try:
		ok = StressHistoryService.delete(rec_id)
		if ok:
			return jsonify({'success': True, 'message': 'Record deleted'})
		return jsonify({'success': False, 'error': 'Record not found'}), 404
	except Exception as e:
		return jsonify({'success': False, 'error': str(e)}), 500


# --- ML model prediction endpoint ---
@main.route('/api/predict-stress', methods=['POST'])
def predict_stress():
	try:
		data = request.get_json() or {}
		# Accept keys: hr, temp, eda
		missing = [k for k in ('hr', 'temp', 'eda') if k not in data]
		if missing:
			return jsonify({'success': False, 'error': f"Missing fields: {', '.join(missing)}"}), 400

		try:
			hr = float(data['hr'])
			temp = float(data['temp'])
			eda = float(data['eda'])
		except Exception:
			return jsonify({'success': False, 'error': 'hr, temp and eda must be numbers'}), 400

		result = StressModelService.predict(hr, temp, eda)

		# Automatically save prediction result to stress_history
		history_data = {
			'hr': result['hr'],
			'temp': result['temp'],
			'eda': result['eda'],
			'label': result['label'],
			'confidence_level': result['confidence_level'],
			'notes': data.get('notes', '')  # Optional notes from request
		}
		saved_history = StressHistoryService.create(history_data)

		return jsonify({
			'success': True,
			'data': result,
			'history_id': saved_history['id']
		})
	except Exception as e:
		return jsonify({'success': False, 'error': str(e)}), 500


# WebSocket-related HTTP endpoints for fallback and testing

@main.route('/api/websocket/info', methods=['GET'])
def websocket_info():
	"""Get WebSocket connection information and endpoints."""
	return jsonify({
		'success': True,
		'websocket_url': '/socket.io/',
		'events': {
			'esp32': {
				'connect_params': '?type=esp32',
				'send_data_event': 'esp32_sensor_data',
				'data_format': {
					'hr': 'float - heart rate',
					'temp': 'float - temperature in celsius',
					'eda': 'float - electrodermal activity',
					'timestamp': 'string/int - ISO format or unix timestamp (optional)',
					'device_id': 'string - device identifier (optional)'
				}
			},
			'frontend': {
				'connect_params': '?type=frontend',
				'listen_events': ['new_sensor_data', 'stress_alert', 'client_stats'],
				'send_events': ['frontend_request_history', 'frontend_subscribe_alerts', 'ping']
			}
		},
		'example_urls': {
			'esp32_connection': 'http://127.0.0.1:5000/socket.io/?type=esp32',
			'frontend_connection': 'http://127.0.0.1:5000/socket.io/?type=frontend'
		}
	})


@main.route('/api/websocket/test', methods=['GET'])
def websocket_test_page():
	"""Serve a simple WebSocket test page."""
	return render_template('websocket_test.html')


@main.route('/api/esp32/data', methods=['POST'])
def esp32_http_fallback():
	"""HTTP fallback endpoint for ESP32 if WebSocket is not available."""
	try:
		data = request.get_json()
		if not data:
			return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

		# Validate required fields
		required_fields = ['hr', 'temp', 'eda']
		missing_fields = [field for field in required_fields if field not in data]
		
		if missing_fields:
			return jsonify({
				'success': False, 
				'error': f'Missing required fields: {", ".join(missing_fields)}'
			}), 400

		# Extract and validate sensor values
		try:
			hr = float(data['hr'])
			temp = float(data['temp'])
			eda = float(data['eda'])
		except (ValueError, TypeError):
			return jsonify({
				'success': False, 
				'error': 'hr, temp, and eda must be valid numbers'
			}), 400

		# Parse timestamp
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

		device_id = data.get('device_id', 'ESP32_HTTP')

		# Perform stress prediction
		try:
			prediction_result = StressModelService.predict_stress({
				'hr': hr,
				'temp': temp,
				'eda': eda
			})
			stress_label = prediction_result.get('prediction', 'unknown')
			confidence = prediction_result.get('confidence', 0.0)
		except Exception as e:
			stress_label = 'error'
			confidence = 0.0

		# Save to database using the existing service
		history_data = {
			'timestamp': timestamp,
			'hr': hr,
			'temp': temp,
			'eda': eda,
			'label': stress_label,
			'confidence_level': confidence,
			'notes': f'HTTP data from {device_id}'
		}
		
		saved_history = StressHistoryService.create(history_data)

		# Return response
		return jsonify({
			'success': True,
			'message': 'Data received and processed successfully',
			'data': {
				'record_id': saved_history['id'],
				'timestamp': timestamp.isoformat(),
				'stress_prediction': {
					'label': stress_label,
					'confidence': round(confidence * 100, 2)
				},
				'sensor_data': {
					'hr': hr,
					'temp': temp,
					'eda': eda
				}
			},
			'note': 'For real-time updates, use WebSocket connection at /socket.io/?type=esp32'
		})

	except Exception as e:
		return jsonify({
			'success': False, 
			'error': f'Server error: {str(e)}'
		}), 500


@main.route('/api/system/status', methods=['GET'])
def system_status():
	"""Get system status including WebSocket connections."""
	try:
		# Get recent data count
		recent_count = StressHistoryService.get_recent_count(hours=24)
		total_count = len(StressHistoryService.get_all())
		
		return jsonify({
			'success': True,
			'status': 'running',
			'features': {
				'websocket': True,
				'http_api': True,
				'stress_prediction': True,
				'real_time_monitoring': True
			},
			'statistics': {
				'total_records': total_count,
				'recent_24h_records': recent_count,
				'last_updated': datetime.now().isoformat()
			},
			'endpoints': {
				'websocket': '/socket.io/',
				'http_esp32_fallback': '/api/esp32/data',
				'websocket_info': '/api/websocket/info',
				'system_status': '/api/system/status'
			}
		})
	except Exception as e:
		return jsonify({
			'success': False,
			'status': 'error',
			'error': str(e)
		}), 500

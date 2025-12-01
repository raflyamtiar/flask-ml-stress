from flask import Blueprint, render_template, request, jsonify
from .service import AppInfoService, StressHistoryService, StressModelService

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
		return jsonify({'success': True, 'data': result})
	except Exception as e:
		return jsonify({'success': False, 'error': str(e)}), 500

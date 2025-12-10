
from flask import Flask
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS


# Initialize extensions here so they can be imported from other modules
db = SQLAlchemy()
from flask_migrate import Migrate

# Migrate extension (initialized in create_app)
migrate = Migrate()
socketio = SocketIO()


def create_app(config_object=None):

	load_dotenv()

	app = Flask(__name__, instance_relative_config=True, template_folder='templates', static_folder='static')
	app.config.from_mapping(
		SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
	)

	app.config.from_pyfile('config.py', silent=True)

	if config_object:
		app.config.from_object(config_object)

	# Ensure instance folder exists (Flask will create it on demand, but ensure DB path)
	try:
		os.makedirs(app.instance_path, exist_ok=True)
	except Exception:
		pass

	# Default database URI if not provided in config
	if not app.config.get('SQLALCHEMY_DATABASE_URI'):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'database.sqlite')
	app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)

	# Initialize extensions
	db.init_app(app)
	migrate.init_app(app, db)
	
	# Initialize CORS for cross-origin requests (React frontend)
	CORS(app, origins="*")
	
	# Initialize SocketIO with CORS support
	socketio.init_app(app, cors_allowed_origins="*", async_mode='eventlet')

	try:
		from .routes import main as main_bp

		app.register_blueprint(main_bp)
	except Exception:
		# If blueprint import fails, we still want the app to be importable
		pass

	# Import models so they are registered on the SQLAlchemy metadata
	# This ensures `flask db migrate --autogenerate` sees the models.
	try:
		from . import models  # noqa: F401
	except Exception:
		pass
		
	# Import events to register SocketIO event handlers
	try:
		from . import events  # noqa: F401
	except Exception:
		pass

	return app


# Export socketio so it can be imported by run.py
__all__ = ['create_app', 'socketio']


from flask import Flask
from dotenv import load_dotenv
import os


def create_app(config_object=None):

	load_dotenv()

	app = Flask(__name__, instance_relative_config=True, template_folder='templates', static_folder='static')
	app.config.from_mapping(
		SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
	)

	app.config.from_pyfile('config.py', silent=True)

	if config_object:
		app.config.from_object(config_object)

	try:
		from .routes import main as main_bp

		app.register_blueprint(main_bp)
	except Exception:
		# If blueprint import fails, we still want the app to be importable
		pass

	return app


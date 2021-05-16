
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
import psycopg2

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Import Blueprints Here
from src.user.routes import upgrade_blueprint

def create_app(config_filename=None):

    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'sa,ple_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mqegptxnpleilm:84cc6f5c616096e414e520b93216f874394d99c3ef9f48da45a8e1a097f4e77a@ec2-52-45-73-150.compute-1.amazonaws.com:5432/d8f8oqefs37jrp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    bootstrap = Bootstrap(app)
    # Initialize app
    db.init_app(app)
    print("initialized db")
    app.register_blueprint(upgrade_blueprint)

    return app

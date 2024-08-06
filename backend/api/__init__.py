import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

load_dotenv()

# cls from flask_sqlalchemy import SQLAlchemy

# instantiate the app
app = Flask(__name__)

# **** Database connection ***************************
url = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = url
# **** JWT Configuration ***************************
app.config["JWT_SECRET_KEY"] = "super-secret-jwt-key"
app.config["UPLOAD_FOLDER"] = "upload/files"

# **** Initialisation  *****************************
jwt = JWTManager(app)
db = SQLAlchemy(app)
# connection = psycopg2.connect(url)

from . import routes

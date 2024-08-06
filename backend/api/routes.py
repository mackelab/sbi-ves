import datetime
import json
from uuid import UUID

from flask import jsonify, request, send_file
from flask_cors import CORS

from . import app
from . import jwt
from .models import User, UserDTO, MeasurementDTO, RegisterUserDTO
from .services import UserService, MeasurementService, FileService, InversionService

from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World! This is Flask  '


# **** Login & Authentication ***********************************************************************************************


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    print("_jwt_header", _jwt_header)
    print("jwt_data", jwt_data)
    identity = jwt_data['id']
    return User.query.filter_by(id=identity).one_or_none()


@app.route('/auth/login', methods=['POST'])
def login():
    auth = request.authorization
    print('auth ', auth)
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = UserService.get_user_by_username(username)
    if not user or not user.check_password(password):
        return jsonify("Wrong username or password"), 401

    # Notice that we are passing in the actual sqlalchemy user object here
    additional_claims = {"id": user.id, "email": user.email, 'username': username}
    access_token = create_access_token(identity=user, additional_claims=additional_claims,
                                       expires_delta=datetime.timedelta(hours=24))
    return jsonify(token=access_token)


# **** User Endpoints **************************************************************************************************

@app.get('/users')
def get_users():
    users = UserService.get_all_users()
    return [UserDTO.model_validate(user) for user in users]


@app.post('/users')
def create_user():
    data = request.get_json()
    user = UserService.create_user(data)
    user_dto = UserDTO.model_validate(user)
    return dict(user_dto)


@app.get('/users/<userId>')
@jwt_required()
def get_user(userId):
    print('userid', userId)
    print('current_user.id', current_user.id)
    if current_user.id == UUID(userId):
        user = UserService.get_user_by_id(userId)
        print("**** user ****", user)
        user_dto = UserDTO.from_orm(user.to_dict())
        return dict(user_dto)
    else:
        print('Do we reach here or is 401 thrown somewhere else?')
        return jsonify("Unauthorized"), 401


# **** Register User ***************************************************************************************************

@app.post('/register')
def register_user():
    user_to_register = RegisterUserDTO.model_validate(request.get_json())
    print("user_to_register", user_to_register)
    # TODO check that username and email are unique and email is valid
    # Check that password equals confirmPassword
    if (user_to_register.password != user_to_register.confirmPassword):
        return jsonify("Passwords do not match"), 400

    registration_user_to_save = user_to_register.to_user()
    user = UserService.save_user(registration_user_to_save)
    user_dto = UserDTO.from_orm(user.to_dict())
    return dict(user_dto)


# **** Measurement Upload **********************************************************************************************

@app.post('/measurements')
@jwt_required()
def save_measurements():
    # **** Validations
    if 'multipart/form-data' not in request.headers['Content-Type']:
        return 'Unsupported Media Type', 415
    if 'file' not in request.files:
        return 'No file part', 400

    # Load the file
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    # Save the file locally and create an instance in the database with metadata
    FileService.save_file_locally(file)
    file_to_save = FileService.create_file_from_upload(file, current_user.id)
    saved_file = FileService.save_file_in_db(file_to_save)

    measurement_data = request.form['measurement']
    measurement = MeasurementService.map_to_measurement(json.loads(measurement_data), file, saved_file)
    saved_measurement = MeasurementService.save_measurement(measurement)
    measurement_dto = MeasurementDTO.model_validate(saved_measurement)
    return dict(measurement_dto), 200


@app.get('/measurements/<measurementId>/inversion/<modelType>')
@jwt_required()
def invert_measurement(measurementId, modelType):
    measurement = MeasurementService.get_measurement_by_id(measurementId)
    filename = InversionService.invert_measurement(measurement, modelType)
    return send_file(filename, mimetype='image/png')
 

# **** Ping Example ****************************************************************************************************


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from auth import Auth
from resume import Resume
import os

UPLOAD_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
jwt = JWTManager(app)

api = Api(app)
api.add_namespace(Auth, '/auth')
api.add_namespace(Resume, '/resume')

if __name__ == "__main__":
    app.run(debug=True)
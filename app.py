from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from auth import Auth_api
from resume import Resume_api
from spec import Spec_api

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

api = Api(app)
api.add_namespace(Auth_api, '/auth')
api.add_namespace(Resume_api, '/resume')
api.add_namespace(Spec_api, '/spec')

if __name__ == "__main__":
    app.run(debug=True)
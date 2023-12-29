from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from auth import Auth_api
from resume import Resume_api
from spec import Spec_api
from post import Post_api
from model import Model_api

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

api = Api(app)
api.add_namespace(Auth_api, '/auth')
api.add_namespace(Resume_api, '/resume')
api.add_namespace(Spec_api, '/spec')
api.add_namespace(Post_api, '/post')
api.add_namespace(Model_api, '/model')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


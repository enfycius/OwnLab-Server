from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from auth import Auth
from resume import Resume

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

api = Api(app)
api.add_namespace(Auth, '/auth')
api.add_namespace(Resume, '/resume')

if __name__ == "__main__":
    app.run(debug=True)
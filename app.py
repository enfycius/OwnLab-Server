from flask import Flask
from flask_restx import Api
from auth import Auth
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

api = Api(app)
api.add_namespace(Auth, '/auth')

if __name__ == "__main__":
    app.run(debug=True)
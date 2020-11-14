from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user_register import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.secret_key = 'Danzilka'

@app.before_first_request
def create_tables():
    db.create_all()

api = Api(app)
jwt = JWT(app, authenticate, identity)

@jwt.auth_response_handler
def custom_response_handler(access_token, identity):
    return jsonify(
        {
            'access_token': access_token.decode('utf-8'),
            'user_id': identity.id
        }
    )

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from db import db

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="Required to be NonZero")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store ID")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "Item not found"}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exist".format(name)}, 400

        data = Item.parser.parse_args()
        
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
            return item.json(), 201
        except:
            return {'message': "An error occured while saving to DB"}, 500

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': "Item deleted"}
        else:
            return {'message': "Item not found."}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': "An error occured while updating the item."}, 500

        return item.json(), 201


class ItemList(Resource):
    def get(self):
        items = ItemModel.query.all()
        # return {'items': [item.json() for item in items]}
        return {'items': list(map(lambda x: x.json(), items))}

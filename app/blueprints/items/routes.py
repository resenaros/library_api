from .schemas import item_schema, items_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Item, db
from . import items_bp



# Items Routes
# Create an item
@items_bp.route("/", methods=['POST'])
def create_item():
    try:
        item_data = item_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Item).where(Item.name == item_data['name']) #Checking our db for an item with this name
    existing_item = db.session.execute(query).scalars().all()
    if existing_item:
        return jsonify({"error": "Item with this name already exists."}), 400

    new_item = Item(**item_data)
    db.session.add(new_item)
    db.session.commit()
    return item_schema.jsonify(new_item), 201

#GET ALL ITEMS
@items_bp.route("/", methods=['GET'])
def get_items():
    query = select(Item)
    items = db.session.execute(query).scalars().all()
    return items_schema.jsonify(items)

#GET SPECIFIC ITEM
@items_bp.route("/<int:item_id>", methods=['GET'])
def get_item(item_id):
    item = db.session.get(Item, item_id)

    if item:
        return item_schema.jsonify(item), 200
    return jsonify({"error": "Item not found."}), 404

#UPDATE SPECIFIC ITEM
@items_bp.route("/<int:item_id>", methods=['PUT'])
def update_item(item_id):
    item = db.session.get(Item, item_id)

    if not item:
        return jsonify({"error": "Item not found."}), 404

    try:
        item_data = item_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in item_data.items():
        setattr(item, key, value)

    db.session.commit()
    return item_schema.jsonify(item), 200

#DELETE SPECIFIC ITEM
@items_bp.route("/<int:item_id>", methods=['DELETE'])
def delete_item(item_id):
    item = db.session.get(Item, item_id)

    if not item:
        return jsonify({"error": "Item not found."}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": f'Item id: {item_id}, successfully deleted.'}), 200
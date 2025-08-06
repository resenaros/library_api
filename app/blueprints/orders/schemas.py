from app.extensions import ma
from app.models import Order, OrderItems
from marshmallow import fields

# SCHEMAS

class ReceiptSchema(ma.Schema):
    '''
    total: 41.06
    order: {
            order_id: 1,
            member_id: 1,
            order_date: "2023-10-01",
            order_items: [
            {
                item:{item_name: "PSL", price:13.02},
                 quantity: 3
            },
            {
                item:{item_name: "Scone", price: 2.00},
                quantity: 1
            }
            ]
            }
    '''
    total = fields.Int(required=True)
    order = fields.Nested("OrderSchema")


# Define the schema for serialization and deserialization
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order #using the SQLAlchemy model to create fields used in serialization, deserialization, and validation
        include_relationships = True  # Include relationships in the schema
    order_items = fields.Nested("OrderItemsSchema", exclude=['id'], many=True)

class OrderItemsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItems #using the SQLAlchemy model to create fields used in serialization, deserialization, and validation
    item = fields.Nested("ItemSchema", exclude=["id"])  # Assuming ItemSchema is defined in items.schemas

class CreateOrderSchema(ma.Schema):
    '''
    {
        member_id: int,
        item_quantity: [{item_id: "1", item_quantity: 2}]
    }
    '''
    member_id = fields.Int(required=True)
    item_quantity = fields.Nested("ItemQuantitySchema", many=True)
    
class ItemQuantitySchema(ma.Schema):
    item_id = fields.Int(required=True)
    item_quantity = fields.Int(required=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True) #variant that allows for the serialization of many Users,
create_order_schema = CreateOrderSchema()
receipt_schema = ReceiptSchema()
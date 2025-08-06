from app.extensions import ma
from app.models import Item

# SCHEMAS
# Define the schema for serialization and deserialization
class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item #using the SQLAlchemy model to create fields used in serialization, deserialization, and validation

item_schema = ItemSchema()
items_schema = ItemSchema(many=True) #variant that allows for the serialization of many Users,
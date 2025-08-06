from app.extensions import ma
from app.models import Member

# SCHEMAS
# Define the schema for serialization and deserialization
class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member #using the SQLAlchemy model to create fields used in serialization, deserialization, and validation
    
member_schema = MemberSchema()
members_schema = MemberSchema(many=True) #variant that allows for the serialization of many Users,
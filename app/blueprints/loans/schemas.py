from marshmallow import fields
from app.extensions import ma
from app.models import Loan

class LoanSchema(ma.SQLAlchemyAutoSchema):
    books = fields.Nested('BookSchema', many=True)
    member = fields.Nested('MemberSchema')
    class Meta:
        model = Loan
        include_relationships = True
        load_instance = True

class EditLoanSchema(ma.Schema):
    add_book_ids = fields.List(fields.Int(), required=True)
    remove_book_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_book_ids", "remove_book_ids")

loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)
return_loan_schema = LoanSchema()  # <-- FIXED here, no exclude
edit_loan_schema = EditLoanSchema()
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Loan, db, Loan, Book
from .schemas import loan_schema, loans_schema, return_loan_schema, edit_loan_schema
from app.blueprints.books.schemas import books_schema  # <-- import here
from . import loans_bp
from app.extensions import limiter

# POST '/' - Create loan
@loans_bp.route('/', methods=['POST'])
def create_loan():
    """
    Create a new loan.
    Expected JSON:
    {
        "vin": "string",
        "ticket_date": "YYYY-MM-DD",
        "customer_id": int
    }
    """
    try:
        loan_data = loan_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_loan = Loan(**loan_data)
    db.session.add(new_loan)
    db.session.commit()
    return loan_schema.jsonify(new_loan), 201

# GET '/' - Get all loans
@loans_bp.route('/', methods=['GET'])
def get_loans():
    query = select(Loan)
    loans = db.session.execute(query).scalars().all()
    return loans_schema.jsonify(loans), 200

# GET '/<loan_id>/books' - Get all books for a specific loan
@loans_bp.route('/<int:loan_id>/books', methods=['GET'])
def get_loan_books(loan_id):
    loan = db.session.get(Loan, loan_id)
    if not loan:
        return jsonify({"error": "Loan not found."}), 404

    return books_schema.jsonify(loan.books), 200

# PUT '/<loan_id>/assign-book/<book_id>' - Assign book to loan
@loans_bp.route('/<int:loan_id>/assign-book/<int:book_id>', methods=['PUT'])
def assign_book(loan_id, book_id):
    loan = db.session.get(Loan, loan_id)
    if not loan:
        return jsonify({"error": "Loan not found."}), 404

    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"error": "book not found."}), 404

    if book not in loan.books:
        loan.books.append(book)
        db.session.commit()
    return loan_schema.jsonify(loan), 200

# PUT '/<loan_id>/remove-book/<book_id>' - Remove book from loan
@loans_bp.route('/<int:loan_id>/remove-book/<int:book_id>', methods=['PUT'])
def remove_book(loan_id, book_id):
    loan = db.session.get(Loan, loan_id)
    if not loan:
        return jsonify({"error": "Loan not found."}), 404

    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({"error": "book not found."}), 404

    if book in loan.books:
        loan.books.remove(book)
        db.session.commit()
        return jsonify({"message": f"Successfully removed book {book_id}: {book.title} from loan {loan_id}."}), 200
    else:
        return jsonify({"error": f"Book {book_id}: {book.title} is not assigned to loan {loan_id}."}), 404

# PATCH '/<loan_id>' - Partially update a loan
@loans_bp.route('/<int:loan_id>', methods=['PATCH'])
@limiter.limit("10/day")  # Limit to 10 requests per day
def patch_loan(loan_id):
    """
    Partially update a loan. Only fields provided in the request will be updated.
    Example JSON:
    {
        "vin": "new vin",
        "ticket_date": "YYYY-MM-DD"
    }
    """
    loan = db.session.get(Loan, loan_id)
    if not loan:
        return jsonify({"error": "Loan not found."}), 404

    if not request.json:
        return jsonify({"error": "No data provided."}), 400

    try:
        loan_data = loan_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    updated = False
    for key, value in loan_data.items():
        if hasattr(loan, key):
            setattr(loan, key, value)
            updated = True

    if not updated:
        return jsonify({"error": "No valid fields provided for update."}), 400

    db.session.commit()
    return loan_schema.jsonify(loan), 200

@loans_bp.route('/<int:loan_id>', methods=['PUT'])
def update_loan(loan_id):
    try:
        loan_edits = edit_loan_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    
    query = select(Loan).where(Loan.id == loan_id)
    loan = db.session.execute(query).scalars().first()
    
    # Add or remove books based on the provided IDs
    for book_id in loan_edits['add_book_ids']:
        query = select(Book).where(Book.id == book_id)
        book = db.session.execute(query).scalars().first()
        if book and book not in loan.books:
            loan.books.append(book)
            
    # Remove books based on the provided IDs
    for book_id in loan_edits['remove_book_ids']:
        query = select(Book).where(Book.id == book_id)
        book = db.session.execute(query).scalars().first()
        if book and book in loan.books:
            loan.books.remove(book)
            
    db.session.commit()
    return loan_schema.jsonify(loan), 200
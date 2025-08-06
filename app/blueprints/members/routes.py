from .schemas import member_schema, members_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Member, db
from . import members_bp
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required

# Login Route
# This route allows a member to log in using their email and password.
@members_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = request.json
        username = credentials['email']
        password = credentials['password']
    except KeyError:
        return jsonify({'messages': 'Invalid payload, expecting username and password'}), 400

    query = select(Member).where(Member.email == username)
    member = db.session.execute(query).scalar_one_or_none() #Query member table for a member with this email

    if member and member.password == password: #if we have a member associated with the username, validate the password
        auth_token = encode_token(member.id)

        response = {
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({'messages': "Invalid email or password"}), 401


# Members Routes
# Create a member
@members_bp.route("/", methods=['POST'])
@limiter.limit("5/day")  # Limit to 5 requests per day
def create_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Member).where(Member.email == member_data['email']) #Checking our db for a member with this email
    existing_member = db.session.execute(query).scalars().all()
    if existing_member:
        return jsonify({"error": "Email already associated with an account."}), 400
    
    new_member = Member(**member_data)
    db.session.add(new_member)
    db.session.commit()
    return member_schema.jsonify(new_member), 201

#GET ALL MEMBERS
@members_bp.route("/", methods=['GET'])
@cache.cached(timeout=30)  # Cache the response for 30 seconds
def get_members():
    query = select(Member)
    members = db.session.execute(query).scalars().all()

    return members_schema.jsonify(members)

#GET SPECIFIC MEMBER
@members_bp.route("/<int:member_id>", methods=['GET'])
def get_member(member_id):
    member = db.session.get(Member, member_id)

    if member:
        return member_schema.jsonify(member), 200
    return jsonify({"error": "Member not found."}), 404

#UPDATE SPECIFIC MEMBER
@members_bp.route("/", methods=['PUT'])
@token_required
@limiter.limit("5/day")  # Limit to 5 requests per day
def update_member(member_id):
    member = db.session.get(Member, member_id)

    if not member:
        return jsonify({"error": "Member not found."}), 404
    
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in member_data.items():
        setattr(member, key, value)

    db.session.commit()
    return member_schema.jsonify(member), 200

#DELETE SPECIFIC MEMBER
@members_bp.route("/", methods=['DELETE'])
@token_required
@limiter.limit("5/day")  # Limit to 5 requests per day
def delete_member(member_id):
    member = db.session.get(Member, member_id)

    if not member:
        return jsonify({"error": "Member not found."}), 404
    
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": f'Member id: {member_id}, successfully deleted.'}), 200
# from crypt import methods
from api.models import User
from api import db
from api import app
from api.services import *
import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask import request, jsonify


@app.route('/api/login', methods=['POST'])
def login():
    """Input: Method Type = GET, {"name":"","password":""}, Return JWT TOKEN {'token': token}"""
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    print(username, password)
    if not username or not password:
        return jsonify({"msg": "Username or Password Missing"}), 409

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"msg": "User not found"}), 409

    if check_password_hash(user.password, password):
        token = jwt.encode({'public_id': user.public_id,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
                           app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({
            "roles": [user.admin],
            "access_token": token,
            "msg": f"Login Successful!, Welcome {username}",
            "username": username,
            "bootcamp": user.bootcamp,
            "cohort": user.cohort,
            "section": user.section
        }), 200

    return jsonify({"msg": "Could not Verify"}), 401


@app.route('/api/add_user', methods=['POST'])
# @token_required
def add_user():
    data = request.get_json()
    if data["secretkey"] == "neduet33iacc44&":
        hashed_password = generate_password_hash(
            data['password'], method='sha256')

        user = User.query.filter_by(username=data["username"]).first()

        if user:
            return jsonify({'msg': 'User already Exists!'}), 409

        new_user = User(public_id=str(uuid.uuid4()),
                        username=data['username'],
                        password=hashed_password, admin=False,
                        bootcamp=data['bootcamp'],
                        cohort=data['cohort'],
                        section=data['section'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'msg': 'New user created!'}), 200

    else:
        return jsonify({'msg': ' Incorrect Secret key'}), 409


@app.route('/api/create_user', methods=['POST'])
# @token_required
def create_user():
    """This endpoint creates a new User, METHOD TYPE = POST, Input RAW JSON {"name":"","password":""}, return {'message': 'New user created!'}"""
    # if not current_user.admin:
    #     return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()

    if data["secretkey"] == "neduet33iacc44&":

        hashed_password = generate_password_hash(
            data['password'], method='sha256')

        user = User.query.filter_by(username=data["username"]).first()

        if user:
            return jsonify({'msg': 'User already Exists!'}), 409

        new_user = User(public_id=str(uuid.uuid4()),
                        username=data['username'], password=hashed_password, admin=True)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'msg': 'New user created!'}), 200

    else:
        return jsonify({'msg': ' Incorrect Secret key'}), 409


@app.route('/api/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    """This endpoint Returns all Users, METHOD TYPE = GET, return {'users': [{"public_id":"<UNIQUE ID>","name":"","password":"<HASHED PASSWORD>","admin": 0 or 1}]}"""
    print(current_user)
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    users = User.query.all()
    print(users)

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['admin'] = user.admin 
        user_data['bootcamp'] = user.bootcamp
        user_data['section'] = user.section
        user_data['cohort'] = user.cohort
        output.append(user_data)

    return jsonify({'users': output})


@app.route('/api/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    """    This endpoint deletes a user,   METHOD TYPE = DELETE,  Input:  public_id of user in url,  RETURN {'message': 'The user has been deleted!'}"""

    if not current_user.admin:
        return jsonify({'msg': 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'msg': 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'msg': 'The user has been deleted!'})


@app.route('/api/get_users', methods=['GET'])
def get_users():
    # """This endpoint Returns all Users, METHOD TYPE = GET, return {'users': [{"public_id":"<UNIQUE ID>","name":"","password":"<HASHED PASSWORD>","admin": 0 or 1}]}"""
    # print(current_user)
    # if not current_user.admin:
    #     return jsonify({'message': 'Cannot perform that function!'})

    users = User.query.all()
    print(users)

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['admin'] = user.admin 
        user_data['bootcamp'] = user.bootcamp
        user_data['section'] = user.section
        user_data['cohort'] = user.cohort
        output.append(user_data)

    return jsonify({'users': output})
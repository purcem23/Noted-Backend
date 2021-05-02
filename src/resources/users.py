from flask import jsonify, request, url_for, redirect, flash
from flask_restful import abort
from flask_login import current_user, login_user, logout_user
from ..config import app, db
from ..models import UserModel
from ..schemas import UserSchema, LoginSchema
import flask_praetorian

guard = flask_praetorian.Praetorian()
guard.init_app(app, UserModel)


# POST one, not limited by id
@app.route("/register", methods=["POST"])
def users_post():
    user = UserSchema().load(request.json)
    result = UserModel.query.filter_by(username=user["username"]).first()
    if not result:
        user = UserModel(**user)
        user.password = guard.hash_password(user.password)
        db.session.add(user)
        db.session.commit()
        return jsonify(UserSchema().dump(user)), 201
    else:
        return jsonify({"message": "Username already exists!"}), 409


@app.route("/login", methods=["POST"])
def login():
    login = LoginSchema().load(request.json)
    user = guard.authenticate(login["username"], login["password"])
    result = jsonify(
        {
            "access_token": guard.encode_jwt_token(user),
            "username": user.username,
        }
    )
    return result, 200


@app.route("/refresh", methods=["POST"])
@flask_praetorian.auth_required
def refresh():
    old_token = request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    result = {"access_token": new_token}
    return result, 200

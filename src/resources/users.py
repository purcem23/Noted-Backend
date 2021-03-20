from flask import jsonify, request, url_for, redirect, flash
from flask_restful import abort
from flask_login import current_user, login_user, logout_user
from ..config import app, db
from ..models import UserModel
from ..schemas import UserSchema, LoginSchema


# GET all method
@app.route('/users', methods=['GET'])
def users_list_get():
    notes = UserModel.query.all()
    return jsonify(UserSchema(many=True).dump(notes))


# GET all by id
@app.route('/users/<int:note_id>', methods=['GET'])
def users_get(user_id):
    result = UserModel.query.filter_by(id=user_id).first()
    if not result:
        abort(404, message='Could not find Note with that ID')
    return jsonify(UserSchema().dump(result))


# POST one, not limited by id
@app.route('/users', methods=['POST'])
def users_post():
    note = UserSchema().load(request.json)
    note = UserModel(**note)
    db.session.add(note)  # add to current session
    db.session.commit()  # commit and make perm, otherwise it temp
    return jsonify(UserSchema().dump(note)), 201  # 201 = created, 200 = ok(nothing broke)


@app.route('/users/<int:note_id>', methods=['PATCH'])
def users_patch(user_id):
    print(request.json)
    note = UserSchema(partial=True).load(request.json)
    # note = NoteModel(**note)
    result = UserModel.query.filter_by(id=user_id).first()
    if not result:
        abort(404, message='Note does not exist, cannot update')
    for key, value in note.items():
        setattr(result, key, value)
    db.session.commit()
    return jsonify(UserSchema().dump(result))


@app.route('/users/<int:note_id>', methods=['DELETE'])
def users_delete(user_id):
    result = UserModel.query.filter_by(id=user_id).first()
    db.session.delete(result)
    db.session.commit()
    return '200'


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if LoginSchema().validate(request.json):
        data = LoginSchema().load(request.json)
        user = UserModel.query.filter_by(username=data["username"]).first()
        if user is None or not user.check_password(data["password"]):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=data["remember_me"])
        return redirect(url_for('index'))
    return redirect(url_for("index"))  # TODO figure out if needed


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
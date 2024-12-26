from flask import request, jsonify
from models import User, db
from schemas import UserSchema
from marshmallow import ValidationError

user_schema = UserSchema()

def init_app(app):
    
    @app.route('/user', methods=['POST'])
    def create_user():
        try:
            data = request.get_json()
            validated_data = user_schema.load(data)
            user = User(**validated_data)
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'User created', 'user_id': user.id}), 201
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400

    @app.route('/user/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify(user_schema.dump(user))
        return jsonify({'message': 'User not found'}), 404

    @app.route('/user/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted'})
        return jsonify({'message': 'User not found'}), 404

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify(user_schema.dump(users, many=True))

from flask import request, jsonify
from data_store import users, user_id_counter
from marshmallow import ValidationError
from schemas import UserSchema

user_schema = UserSchema()

def init_app(app):
    
    @app.route('/user', methods=['POST'])
    def create_user():
        global user_id_counter
        try:
            data = request.get_json()
            validated_data = user_schema.load(data)
            user = {'id': user_id_counter, 'name': validated_data['name']}
            users[user_id_counter] = user
            user_id_counter += 1
            return jsonify({'message': 'User created', 'user_id': user['id']}), 201
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400

    @app.route('/user/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = users.get(user_id)
        if user:
            return jsonify(user)
        return jsonify({'message': 'User not found'}), 404

    @app.route('/user/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        if user_id in users:
            del users[user_id]
            return jsonify({'message': 'User deleted'})
        return jsonify({'message': 'User not found'}), 404

    @app.route('/users', methods=['GET'])
    def get_users():
        return jsonify(list(users.values()))

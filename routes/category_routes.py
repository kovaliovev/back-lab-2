from flask import request, jsonify
from data_store import categories, category_id_counter
from marshmallow import ValidationError
from schemas import CategorySchema

category_schema = CategorySchema()

def init_app(app):
    
    @app.route('/category', methods=['POST'])
    def create_category():
        global category_id_counter
        try:
            data = request.get_json()
            validated_data = category_schema.load(data)
            category = {'id': category_id_counter, 'name': validated_data['name']}
            categories[category_id_counter] = category
            category_id_counter += 1
            return jsonify({'message': 'Category created', 'category_id': category['id']}), 201
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400

    @app.route('/category', methods=['GET'])
    def get_categories():
        return jsonify(list(categories.values()))

    @app.route('/category', methods=['DELETE'])
    def delete_category():
        data = request.get_json()
        category_id = data.get('category_id')
        if category_id in categories:
            del categories[category_id]
            return jsonify({'message': 'Category deleted'})
        return jsonify({'message': 'Category not found'}), 404
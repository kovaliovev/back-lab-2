from flask import request, jsonify
from data_store import categories, category_id_counter

def init_app(app):
    
    @app.route('/category', methods=['POST'])
    def create_category():
        global category_id_counter
        data = request.get_json()
        category = {'id': category_id_counter, 'name': data['name']}
        categories[category_id_counter] = category
        category_id_counter += 1
        return jsonify({'message': 'Category created', 'category_id': category['id']}), 201

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
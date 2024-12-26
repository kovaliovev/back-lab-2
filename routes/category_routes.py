from flask import request, jsonify
from models import Category, db
from schemas import CategorySchema
from marshmallow import ValidationError

category_schema = CategorySchema()

def init_app(app):
    
    @app.route('/category', methods=['POST'])
    def create_category():
        try:
            data = request.get_json()
            validated_data = category_schema.load(data)
            category = Category(**validated_data)
            db.session.add(category)
            db.session.commit()
            return jsonify({'message': 'Category created', 'category_id': category.id}), 201
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400

    @app.route('/category', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        return jsonify(category_schema.dump(categories, many=True))

    @app.route('/category/<int:category_id>', methods=['GET'])
    def get_category(category_id):
        category = Category.query.get(category_id)
        if category:
            return jsonify(category_schema.dump(category))
        return jsonify({'message': 'Category not found'}), 404

    @app.route('/category/<int:category_id>', methods=['DELETE'])
    def delete_category(category_id):
        category = Category.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return jsonify({'message': 'Category deleted'})
        return jsonify({'message': 'Category not found'}), 404

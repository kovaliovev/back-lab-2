from flask import request, jsonify
from models import Category, User, db
from schemas import CategorySchema
from marshmallow import ValidationError

category_schema = CategorySchema()

def init_app(app):
    
    @app.route('/category', methods=['POST'])
    def create_category():
        try:
            data = request.get_json()
            validated_data = category_schema.load(data)

            is_global = validated_data.get('is_global', True)
            user_id = validated_data.get('user_id', None) if not is_global else None

            if not is_global and not User.query.get(user_id):
                return jsonify({'message': 'User not found'}), 404

            category = Category(
                name=validated_data['name'],
                is_global=is_global,
                user_id=user_id
            )
            db.session.add(category)
            db.session.commit()

            return jsonify({'message': 'Category created', 'category_id': category.id}), 201
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400

    @app.route('/categories', methods=['GET'])
    def get_categories():
        user_id = request.args.get('user_id', type=int)

        if user_id:
            categories = Category.query.filter(
                (Category.is_global == True) | (Category.user_id == user_id)
            ).all()
        else:
            categories = Category.query.filter_by(is_global=True).all()

        return jsonify(category_schema.dump(categories, many=True))

    @app.route('/category/<int:category_id>', methods=['DELETE'])
    def delete_category(category_id):
        category = Category.query.get(category_id)
        if category:
            if not category.is_global:
                db.session.delete(category)
                db.session.commit()
                return jsonify({'message': 'Category deleted'})
            else:
                return jsonify({'message': 'Global categories cannot be deleted'}), 403
        return jsonify({'message': 'Category not found'}), 404

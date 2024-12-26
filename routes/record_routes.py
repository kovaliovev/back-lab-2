from flask import request, jsonify
from datetime import datetime
from models import Record, User, Category, db
from schemas import RecordSchema
from marshmallow import ValidationError

record_schema = RecordSchema()

def init_app(app):
    
    @app.route('/record', methods=['POST'])
    def create_record():
        try:
            data = request.get_json()
            validated_data = record_schema.load(data)
            
            record = Record(
                user_id=validated_data['user_id'],
                category_id=validated_data['category_id'],
                timestamp=datetime.now(),
                amount=validated_data['amount']
            )
            db.session.add(record)
            db.session.commit()

            return jsonify({'message': 'Record created', 'record_id': record.id}), 201
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400

    @app.route('/record/<int:record_id>', methods=['GET'])
    def get_record(record_id):
        record = Record.query.get(record_id)
        if record:
            return jsonify(record_schema.dump(record))
        return jsonify({'message': 'Record not found'}), 404

    @app.route('/record/<int:record_id>', methods=['DELETE'])
    def delete_record(record_id):
        record = Record.query.get(record_id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return jsonify({'message': 'Record deleted'})
        return jsonify({'message': 'Record not found'}), 404

    @app.route('/record', methods=['GET'])
    def get_records():
        user_id = request.args.get('user_id')
        category_id = request.args.get('category_id')

        query = Record.query

        if user_id:
            query = query.filter_by(user_id=user_id)
        if category_id:
            query = query.filter_by(category_id=category_id)

        records = query.all()

        if not records:
            return jsonify({'message': 'No records found'}), 404

        return jsonify(record_schema.dump(records, many=True))

from flask import request, jsonify
from datetime import datetime
from data_store import records, record_id_counter
from marshmallow import ValidationError
from schemas import RecordSchema

record_schema = RecordSchema()

def init_app(app):
    
    @app.route('/record', methods=['POST'])
    def create_record():
        global record_id_counter
        try:
            data = request.get_json()
            validated_data = record_schema.load(data)
            record = {
                'id': record_id_counter,
                'user_id': validated_data['user_id'],
                'category_id': validated_data['category_id'],
                'timestamp': datetime.now().isoformat(),
                'amount': validated_data['amount']
            }
            records[record_id_counter] = record
            record_id_counter += 1
            return jsonify({'message': 'Record created', 'record_id': record['id']}), 201
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400

    @app.route('/record/<int:record_id>', methods=['GET'])
    def get_record(record_id):
        record = records.get(record_id)
        if record:
          return jsonify(record)
        return jsonify({'message': 'Record not found'}), 404

    @app.route('/record/<int:record_id>', methods=['DELETE'])
    def delete_record(record_id):
        if record_id in records:
            del records[record_id]
            return jsonify({'message': 'Record deleted'})
        return jsonify({'message': 'Record not found'}), 404

    @app.route('/record', methods=['GET'])
    def get_records():
        user_id = request.args.get('user_id')
        category_id = request.args.get('category_id')

        if not user_id and not category_id:
            return jsonify({'message': 'user_id or category_id required'}), 400

        filtered_records = list(records.values())

        if user_id:
            filtered_records = [r for r in filtered_records if r['user_id'] == int(user_id)]
        if category_id:
            filtered_records = [r for r in filtered_records if r['category_id'] == int(category_id)]

        if not filtered_records:
            return jsonify({'message': 'No records found'}), 404

        return jsonify(filtered_records)
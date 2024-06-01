from flask import Flask, request, jsonify
import boto3
import os
import uuid

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

@app.route('/createUser', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = str(uuid.uuid4())
    item = {
        'userId': user_id,
        'name': data['name'],
        'email': data['email']
    }
    table.put_item(Item=item)
    return jsonify(item), 201

@app.route('/getUserById/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    response = table.get_item(
        Key={
            'userId': user_id
        }
    )
    item = response.get('Item')
    if not item:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(item)

def handler(event, context):
    return app(event, context)

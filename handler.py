
from flask import Flask, request, jsonify
import boto3
import os
import uuid

app = Flask(__name__)

# Inizializzazione delle risorse AWS
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


@app.route('/createUser', methods=['POST'])
def create_user():
    """
    Crea un nuovo utente nel database DynamoDB.

    Payload della richiesta (JSON):
    {
        "name": "Nome utente",
        "email": "email@example.com"
    }

    Risposta (JSON):
    {
        "userId": "ID utente generato",
        "name": "Nome utente",
        "email": "email@example.com"
    }
    """
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
    """
    Ottiene le informazioni di un utente dal database DynamoDB utilizzando l'ID utente.

    Parametri della richiesta:
    - user_id: ID utente

    Risposta (JSON):
    {
        "userId": "ID utente",
        "name": "Nome utente",
        "email": "email@example.com"
    }
    """
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
    """
    Funzione di gestione per l'esecuzione su AWS Lambda.
    """
    return app(event, context)



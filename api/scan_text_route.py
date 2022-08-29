from api.models import User
from api import db
from api import app
from api.services import *
from functools import wraps
import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask_expects_json import expects_json
from flask import Flask, request, jsonify, make_response
import base64
from pathlib import Path
import os
Path(os.path.join('.', 'download')).mkdir(parents=True, exist_ok=True)

schema = {
    'type': 'object',
    'properties': {
        'name': {'text': 'string',
                 'img': 'string'}
    },
    'required': ['text', 'img']
}


@app.route('/api/scan_text', methods=['POST'])
@token_required
@expects_json(schema)
def scan_text(current_user):
    data = request.get_json()
    filepath = os.path.join('.', 'download', 'imageToSave.png')
    imgdata = base64.b64decode(data['img'].replace('data:image/png;base64,',''))
    with open(filepath, "wb") as fh:
        fh.write(imgdata)

    return jsonify({"result": True})

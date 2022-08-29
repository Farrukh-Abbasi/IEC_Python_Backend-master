from api.models import User, StudentTable, Cohorts, Bootcamp
from flask import Flask, json, request, jsonify,url_for
from api import db
import os
import urllib.request
import pandas as pd
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False  

app.secret_key = "key-file"
 
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['txt', 'csv','pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/')
def main():
    return 'Homepage'
 
@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has tthe file part
    if 'files' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
 
    files = request.files.getlist('files')
     
    errors = {}
    success = False
     
    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            generate_1(filename)
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'
 
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({'message' : 'Files successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp

def generate_1(filename):
    # Read data from CSVs
    df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    list_of_students = df.to_dict('records')  # This will receive the list of objects
    list_of_models = []
    for i in list_of_students:
        list_of_models.append(StudentTable(
            name=i['name'],
            cohort_id=i['cohort_id'],
            bootcamp_id=i['bootcamp_id'],
            gr=i['gr'],
            email=i['email'],
            city=i['city'],
            financial_aid=i['financial_aid'],
            current_status=i['current_status']

        )) 

    db.session.add_all(list_of_models)
    db.session.commit()
if __name__ == '__main__':
    app.run(debug=True)
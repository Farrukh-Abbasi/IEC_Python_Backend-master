import pdfkit
import os
from flask import Flask, request, jsonify, make_response, render_template
from api import db
from api import app
from api.models import ParseStudent, StudentCertificate, Bootcamp, Cohorts, StudentTable
from api.studentRoutes import studentParser
from flask_cors import cross_origin
from api.passed_students import passed
from api.certificateCreation import *
from api.email_script import EmailThread
import imgkit
from datetime import date

API_URL = "https://lnd.iec.org.pk"


def certificate_data_parser(student):
    student_dict = dict()
    student_dict['id'] = student.id
    student_dict['gr'] = student.gr
    student_dict['email'] = student.email
    student_dict['name'] = student.name
    student_dict['city'] = student.city
    student_dict['verified'] = student.verified
    student_dict['bootcamp'] = student.bootcamp
    student_dict['cohort'] = student.cohort
    return student_dict


@app.route('/api/create_certificate_png/<id>', methods=['GET'])
def create_certificate_png(id):
    student_certificate = StudentCertificate.query.filter_by(
        id=id).first()
    student = {
        "date": date.today().strftime("%B %d, %Y"),
        "name": student_certificate.name,
        "courseName": student_certificate.bootcamp
    }
    html = render_template('certificate.html', student=student)
    imgkit.from_string(html, 'api/static/certificates/' + str(id) + '.png')
    return 'certificate_created'


@app.route('/api/create_certificate_pdf/<id>', methods=['GET'])
def create_certificate_pdf(id):
    student_certificate = StudentCertificate.query.filter_by(
        id=id).first()
    student = {
        "date": date.today().strftime("%B %d, %Y"),
        "name": student_certificate.name,
        "courseName": student_certificate.bootcamp
    }

    return render_template('certificate.html', student=student)


@app.route('/api/create_certificate', methods=['GET'])
def create_certificate():
    # student = request.get_json()
    student = {
        "date": date.today().strftime("%B %d, %Y"),
        "name": "John Doe",
        "courseName": "Web Development"
    }

    rendered = render_template('certificate.html', student=student)

    print(type(rendered))
    print(rendered)
    return rendered


@app.route('/api/get_data_certificate/<id>', methods=['GET'])
def get_data_certificate(id):
    student_certificate = StudentCertificate.query.filter_by(
        id=id).first()
    if student_certificate:
        return jsonify(
            {"message": "Student added successfully", 'data': certificate_data_parser(student_certificate)}), 200

    else:
        return jsonify({"message": "Student not found"}), 404


# This is working


@app.route('/api/save_certificate', methods=['POST'])
def save_certificate():
    data = request.get_json()
    new_student = StudentCertificate(
        gr=data["gr"],
        email=data["email"],
        name=data["name"],
        city=data["city"],
        verified=1,
        bootcamp=data["bootcamp"],
        cohort=data["cohort"]
    )
    db.session.add(new_student)
    db.session.commit()

    student = {
        "date": date.today().strftime("%B %d, %Y"),
        "name": new_student.name,
        "courseName": new_student.bootcamp
    }

    html = render_template('certificate.html', student=student)

    imgkit.from_string(html, 'api/static/certificates/' +
                       str(new_student.id) + '.png')

    pdfkit.from_string(html, 'api/static/pdfs/' +
                       str(new_student.id) + '.pdf')

    certificate_url = API_URL + \
                      "/api/create_certificate_pdf/" + str(new_student.id)
    EmailThread(data["email"], new_student.id, certificate_url).start()

    print("Certificate added")

    return jsonify({"message": "Student added successfully", "certificate_id": new_student.id}), 200


@app.route('/api/get_certificate', methods=['POST'])
def get_certificate():
    data = request.get_json()
    if 'gr' in data:
        data = request.get_json()
        student = StudentTable.query.filter_by(gr=data['gr']).first()
        if student:
            if student.passed:
                student_certificate = StudentCertificate.query.filter_by(
                    gr=data['gr']).first()
                if student_certificate:
                    certficateData = certificate_data_parser(
                        student_certificate)
                    return jsonify({
                        'data': certficateData,
                        'message': 'Certificate found',
                        'id': 3,
                    }), 200
                else:
                    return jsonify(
                        {'data': studentParser(student), 'message': 'Student does not have certificate', 'id': 1}), 200
            else:
                return jsonify({
                    'data': {},
                    'message': 'Student not passed', 'id': 5}), 200

        else:
            return jsonify({'message': 'Student does not exist', 'id': 0}), 200
    else:
        return jsonify({'message': 'Please provide a correct GR number', 'id': 2}), 200


@app.route('/api/delete_certificate/<id>', methods=['GET'])
def delete_certificate(id):
    print(id)
    student_certificate = StudentTable.query.filter_by(id=id).first()
    student_gr = student_certificate.gr
    print(student_gr)
    certificate = StudentCertificate.query.filter_by(gr=student_gr).first()
    if certificate:
        certificate_data = certificate_data_parser(certificate)
        print(certificate_data)
        db.session.delete(certificate)
        db.session.commit()
        return jsonify({"message": "Certificate deleted successfully"}), 200
    else:
        return jsonify({"message": "Certificate Not Found"}), 200


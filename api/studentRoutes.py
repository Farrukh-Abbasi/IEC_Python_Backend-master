from requests import session
from api.models import User, StudentTable, Bootcamp, Cohorts, ParseStudent
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


def studentParser(student):
    student_dict = dict()
    # student_dict['id'] = student.id
    # student_dict['gr'] = student.gr
    # student_dict['email'] = student.email
    # student_dict['projectAttendance'] = student.projectAttendance
    # student_dict['careerReadiness'] = student.careerReadiness
    # student_dict['attendance'] = student.attendance
    # student_dict['bootcampCompletion'] = student.bootcampCompletion
    # student_dict['instructorRating'] = student.instructorRating
    # student_dict['CommunicationInterview'] = student.CommunicationInterview
    # student_dict['comments'] = student.comments
    # student_dict['overallGrading'] = student.overallGrading
    # student_dict['bootcamp_id'] = student.bootcamp_id
    # student_dict['cohort_id'] = student.cohort_id

    student_dict['id'] = student.id
    student_dict['gr'] = student.gr
    student_dict['email'] = student.email
    student_dict['name'] = student.name
    student_dict['city'] = student.city
    student_dict['financial_aid'] = student.financial_aid
    student_dict['current_status'] = student.current_status
    student_dict['bootcamp'] = student.bootcamp.name
    student_dict['passed'] = student.passed
    student_dict['bootcamp_id'] = student.bootcamp.id
    student_dict['cohort'] = student.cohort_id
    return student_dict


@app.route('/api/get_bootcamp_students/<bootcampId>')
def get_bootcamp_students(bootcampId):
    bootcampStudents = StudentTable.query.filter_by(
        bootcamp_id=bootcampId).all()
    students_list = []
    for student in bootcampStudents:
        student_dict = studentParser(student)
        students_list.append(student_dict)

    return jsonify(students_list), 200


@app.route('/api/get_bootcamps/<cohort_id>', methods=['GET'])
def get_bootcamps(cohort_id):
    bootcamp = Bootcamp.query.filter_by(cohort_id=cohort_id).all()
    output = []
    students_list = []
    for i in bootcamp:
        bootcamp_data = dict()
        bootcamp_data['id'] = i.id
        bootcamp_data['name'] = i.name
        bootcamp_data['section'] = i.section
        bootcamp_data['cohort_id'] = i.cohort_id
        for student in i.students:
            student_dict = studentParser(student)
            students_list.append(student_dict)
        output.append(bootcamp_data)

    return jsonify({"output": output, "students_list": students_list}), 200


@app.route('/api/get_cohorts', methods=['GET'])
def get_cohort():
    cohorts = Cohorts.query.all()
    output = []
    students_list = []
    for i in cohorts:
        cohort_data = {}

        cohort_data['id'] = i.id
        cohort_data['cohort'] = i.cohort
        for student in i.student:
            student_dict = studentParser(student)
            students_list.append(student_dict)
        output.append(cohort_data)
    return jsonify({"output": output, "students": students_list}), 200


# @app.route('/api/editRow', methods=['POST'])
# def update_student():
#     data = request.get_json()
#     student = StudentTable.query.filter_by(id=data["id"])
#     student.gr = data["gr"]
#     student.email = data["email"]
#     student.name = data["name"]
#     student.city = data["city"]
#     student.financial_aid = data["financial_aid"]
#     student.current_status = data["current_status"]
#     db.session.commit()
#     print(data)
#     return jsonify({"msg": "Success"}), 200


@app.route('/api/editRow', methods=['POST'])
def update_student():
    data = request.get_json()
    print(data)
    student = StudentTable.query.filter_by(id=data["id"]).update({
        'gr': data["gr"],
        'email': data["email"],
        'name': data["name"],
        'city': data["city"],
        'financial_aid': data["financial_aid"],
        'current_status': data["current_status"],
        'passed': data['passed']

    })
    db.session.commit()
    print(data)
    return jsonify({"msg": "Success"}), 200


@app.route('/api/get_cohorts_only', methods=['GET'])
def get_cohort_only():
    cohorts = Cohorts.query.all()
    output = []
    for i in cohorts:
        cohort_data = {}

        cohort_data['id'] = i.id
        cohort_data['cohort'] = i.cohort
        output.append(cohort_data)
    return jsonify({"output": output}), 200


@app.route('/api/get_bootcamps_only/<cohort_id>', methods=['GET'])
def get_bootcamp_only(cohort_id):
    bootcamps = Bootcamp.query.filter_by(cohort_id=cohort_id).all()
    output = []
    for i in bootcamps:
        bootcamp_data = {}

        bootcamp_data['id'] = i.id
        bootcamp_data['name'] = i.name
        output.append(bootcamp_data)
    return jsonify({"output": output}), 200


@app.route('/api/save_student', methods=['POST'])
def save_student():
    data = request.get_json()
    print(data)
    new_student = StudentTable(
        gr=data["gr"],
        email=data["email"],
        name=data["name"],
        city=data["city"],
        financial_aid=data["financial_aid"],
        current_status=data["current_status"],
        bootcamp_id=data["bootcamp_id"],
        cohort_id=data["cohort_id"]
    )
    db.session.add(new_student)
    db.session.commit()
    print("User added")

    return jsonify({"message": "Student added successfully"}), 200


@app.route('/api/delete_student/<id>', methods=['GET'])
def delete_student(id):
    student = StudentTable.query.filter_by(id=id).first()
    print(student.id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"}), 200

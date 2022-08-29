import email
from email.policy import default
from unicodedata import category

from importlib_metadata import Sectioned
from api import db
from datetime import datetime, date


class ParseStudent:
    id = ""
    gr = ""
    email = ""
    projectAttendance = ""
    careerReadiness = ""
    attendance = ""
    bootcampCompletion = ""
    instructorRating = ""
    CommunicationInterview = ""
    comments = ""
    overallGrading = ""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(256))
    admin = db.Column(db.Boolean)
    bootcamp = db.Column(db.Integer)
    cohort = db.Column(db.Integer)
    section = db.Column(db.Integer)


class StudentCertificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gr = db.Column(db.String(100))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    bootcamp = db.Column(db.String(100))
    cohort = db.Column(db.Integer)
    city = db.Column(db.String(100))
    verified = db.Column(db.Boolean, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_updated = db.Column(db.DateTime, default=datetime.now())


class Cohorts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cohort = db.Column(db.Integer)
    bootcamp = db.relationship('Bootcamp', backref='cohorts')
    student = db.relationship('StudentTable', backref='cohorts')


class Bootcamp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    section = db.Column(db.Integer, default=0)
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id'))
    students = db.relationship('StudentTable', backref='bootcamp')


# class StudentTable(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     gr = db.Column(db.String(80))
#     email = db.Column(db.String(100))
#     projectAttendance = db.Column(db.Boolean, default=0)
#     careerReadiness = db.Column(db.Integer)
#     attendance = db.Column(db.Float)
#     bootcampCompletion = db.Column(db.Float)
#     instructorRating = db.Column(db.Integer)
#     CommunicationInterview = db.Column(db.Boolean, default=0)
#     comments = db.Column(db.String(500))
#     overallGrading = db.Column(db.Integer)
#     bootcamp_id = db.Column(db.Integer, db.ForeignKey('bootcamp.id'))
#     cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id'))

class StudentTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gr = db.Column(db.String(80))
    email = db.Column(db.String(100))
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    financial_aid = db.Column(db.String(50))
    current_status = db.Column(db.String(50))
    passed = db.Column(db.Boolean)
    bootcamp_id = db.Column(db.Integer, db.ForeignKey('bootcamp.id'))
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id'))
    attendance = db.relationship('AttendanceTable', backref='student_table')


class AttendanceTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today())
    attendance = db.Column(db.Integer, default=2)
    category = db.Column(db.String(50))
    tech_sess1 = db.Column(db.Integer, default=2)
    tech_sess2 = db.Column(db.Integer, default=2)
    mentor_session = db.Column(db.Integer, default=2)
    eecs_session = db.Column(db.Integer, default=2)
    career_session = db.Column(db.Integer, default=2)
    sessions_missed = db.Column(db.Integer, default=0)

    student_id = db.Column(db.Integer, db.ForeignKey('student_table.id'))


class DropoutTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gr = db.Column(db.String(80))
    name = db.Column(db.String(100))
    stage = db.Column(db.String(50))
    section = db.Column(db.Integer)
    email = db.Column(db.String(100))
    date = db.Column(db.Date, default=date.today())
    reason = db.Column(db.String(100))


class ProjectTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gr = db.Column(db.String(80))
    name = db.Column(db.String(100))
    section = db.Column(db.Integer)
    category = db.Column(db.String(50))
    projectstatus = db.Column(db.String(50))
    evaluationstatus = db.Column(db.String(50))
    project = db.Column(db.String(50))
    instructorgrade = db.Column(db.String(50))
    evaluatorgrade = db.Column(db.String(50))
    comments = db.Column(db.String(100))

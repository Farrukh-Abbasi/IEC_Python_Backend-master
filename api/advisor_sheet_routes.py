from datetime import datetime, date
from api import db
from api.models import DropoutTable, StudentTable, AttendanceTable, ProjectTable
from api import app
from flask import Flask, request, jsonify


@app.route("/api/advisor/add_dropout", methods=["POST"])
def dropout_student():
    data = request.get_json()

    StudentTable.query.filter_by(gr=data["gr"]).update(
        {
            "current_status": "Dropped",
        }
    )

    try:
        dateObj = datetime.strptime(data["dropdate"], "%Y-%m-%d").date()
    except:
        dateObj = date.today()
    new_student = DropoutTable(
        name=data["name"],
        gr=data["gr"],
        email=data["email"],
        section=data["section"],
        stage=data['dropoutstage'],
        reason=data["dropoutreason"],
        date=dateObj,
    )
    db.session.add(new_student)
    db.session.commit()

    return jsonify({"msg": "Success"}), 200


@app.route("/api/advisor/edit_dropout", methods=["POST"])
def edit_dropout():
    data = request.get_json()
    try:
        dateObj = datetime.strptime(data["dropdate"], "%Y-%m-%d").date()
    except:
        dateObj = date.today()
    new_student = DropoutTable.query.filter_by(gr=data["gr"]).update(
        {
            "name": data["name"],
            "gr": data["gr"],
            "email": data["email"],
            "stage": data["dropoutstage"],
            "section": data["section"],
            "reason": data["dropoutreason"],
            "date": dateObj,
        }
    )

    db.session.commit()

    return jsonify({"msg": "Success"}), 200


@app.route("/api/advisor/get_dropped_students", methods=["GET"])
def get_dropped_students():
    cohorts = DropoutTable.query.all()
    output = []
    for i in cohorts:
        cohort_data = {}

        cohort_data["id"] = i.id
        cohort_data["name"] = i.name
        cohort_data["section"] = i.section
        cohort_data['dropoutstage'] = i.stage
        cohort_data["dropoutreason"] = i.reason
        cohort_data["dropdate"] = i.date.strftime("%Y-%m-%d")
        cohort_data["gr"] = i.gr
        output.append(cohort_data)
    return jsonify({"output": output}), 200


@app.route("/api/advisor/add_attendance", methods=["POST"])
def add_attendance():
    data = request.get_json()

    if not data["students"]:
        return jsonify({"msg": "No Data Recieved"}), 200
    else:
        attendance_check = AttendanceTable.query.filter_by(
            date=datetime.strptime(data["meta"]["date"], "%Y-%m-%d").date(),
            student_id=data["students"][0]["id"],
        ).all()
        if attendance_check:
            return jsonify({"msg": "Data Already Exist for today!"}), 200
        else:
            models_list = []
            for student in data["students"]:
                models_list.append(
                    AttendanceTable(
                        student_id=student["id"],
                        date=datetime.strptime(data["meta"]["date"], "%Y-%m-%d").date(),
                        attendance=student["attendance"],
                        category=student["category"],
                        tech_sess1=student["tech_sess1"],
                        tech_sess2=student["tech_sess2"],
                        mentor_session=student["mentor_session"],
                        eecs_session=student["eecs_session"],
                        career_session=student["career_session"],
                    )
                )
            db.session.add_all(models_list)
            db.session.commit()

        return jsonify({"msg": "Success, Data updated"}), 200


@app.route("/api/advisor/search_students", methods=["POST"])
def search_students():
    data = request.get_json()
    if data:
        student_dict = {}
        start_date = datetime.strptime(data["searchStartDate"], "%Y-%m-%d").date()
        end_date = datetime.strptime(data["searchEndDate"], "%Y-%m-%d").date()
        attendance_rows = (
            AttendanceTable.query.filter(AttendanceTable.date <= end_date)
            .filter(AttendanceTable.date >= start_date)
            .all()
        )

        for atd in attendance_rows:
            if atd.student_id not in student_dict.keys():
                session_missed = 0
                student_dict[atd.student_id] = {
                    "student_id": atd.student_id,
                    "attendance": atd.attendance if atd.attendance != 2 else 0,
                    "category": atd.category,
                    "tech_sess1": atd.tech_sess1 if atd.tech_sess1 != 2 else 0,
                    "tech_sess2": atd.tech_sess2 if atd.tech_sess2 != 2 else 0,
                    "mentor_session": atd.mentor_session
                    if atd.mentor_session != 2
                    else 0,
                    "eecs_session": atd.eecs_session if atd.eecs_session != 2 else 0,
                    "career_session": atd.career_session
                    if atd.career_session != 2
                    else 0,
                    "sessions_missed": 0,
                }

                student_dict[atd.student_id]["sessions_missed"] = (
                    1 - atd.attendance
                    if atd.attendance != 2
                    else 1 + 1 - atd.tech_sess1
                    if atd.tech_sess1 != 2
                    else 1 + 1 - atd.tech_sess2
                    if atd.tech_sess2 != 2
                    else 1 + 1 - atd.mentor_session
                    if atd.mentor_session != 2
                    else 1 + 1 - atd.eecs_session
                    if atd.eecs_session != 2
                    else 1 + 1 - atd.career_session
                    if atd.career_session != 2
                    else 1
                )

            else:
                if atd.attendance != 2:
                    student_dict[atd.student_id]["attendance"] += atd.attendance
                    student_dict[atd.student_id]["sessions_missed"] += (
                        1 if atd.attendance == 0 else 0
                    )

                if atd.category:
                    student_dict[atd.student_id]["category"] = atd.category

                if atd.tech_sess1 != 2:
                    student_dict[atd.student_id]["tech_sess1"] += atd.tech_sess1
                    student_dict[atd.student_id]["sessions_missed"] += (
                        1 if atd.tech_sess1 == 0 else 0
                    )

                if atd.tech_sess2 != 2:
                    student_dict[atd.student_id]["tech_sess2"] += atd.tech_sess2
                    student_dict[atd.student_id]["sessions_missed"] += (
                        1 if atd.tech_sess2 == 0 else 0
                    )

                if atd.mentor_session != 2:
                    student_dict[atd.student_id]["mentor_session"] += atd.mentor_session
                    student_dict[atd.student_id]["sessions_missed"] += (
                        1 if atd.mentor_session == 0 else 0
                    )

                if atd.eecs_session != 2:
                    student_dict[atd.student_id]["eecs_session"] += atd.eecs_session
                    student_dict[atd.student_id]["sessions_missed"] += (
                        1 if atd.eecs_session == 0 else 0
                    )

                if atd.career_session != 2:
                    student_dict[atd.student_id]["career_session"] += atd.career_session
                    student_dict[atd.student_id]["sessions_missed"] += (
                        1 if atd.career_session == 0 else 0
                    )

        return jsonify({"msg": "Success", "students": student_dict}), 200

    else:
        return jsonify({"msg": "No Data Recieved"}), 200


@app.route("/api/advisor/add_project", methods=["POST"])
def student_project():
    data = request.get_json()
    # print("Data: ",data)
    new_student = ProjectTable(
        name=data["name"],
        gr=data["gr"],
        section=data["section"],
        category=data["category"],
        projectstatus=data["project_status"],
        evaluationstatus=data["evaluation_status"],
        project=data["project"],
        instructorgrade=data["instructor_grade"],
        evaluatorgrade=data["evaluator_grade"],
        comments=data["project_comments"],
    )
    db.session.add(new_student)
    db.session.commit()

    return jsonify({"msg": "Success"}), 200


@app.route("/api/advisor/edit_project", methods=["POST"])
def edit_project():
    data = request.get_json()
    new_student = ProjectTable.query.filter_by(gr=data["gr"]).update(
        {
            "name": data["name"],
            "gr": data["gr"],
            "section": data["section"],
            "category": data["category"],
            "projectstatus": data["project_status"],
            "evaluationstatus": data["evaluation_status"],
            "project": data["project"],
            "instructorgrade": data["instructor_grade"],
            "evaluatorgrade": data["evaluator_grade"],
            "comments": data["project_comments"],
        }
    )

    db.session.commit()

    return jsonify({"message": "Success"}), 200


@app.route("/api/advisor/get_projects", methods=["GET"])
def get_student_projects():
    cohorts = ProjectTable.query.all()
    output = []
    for i in cohorts:
        cohort_data = {}

        cohort_data["id"] = i.id
        cohort_data["name"] = i.name
        cohort_data["gr"] = i.gr
        cohort_data["section"] = i.section
        cohort_data['category'] = i.category
        cohort_data["project"] = i.project
        cohort_data["project_status"] = i.projectstatus
        cohort_data["evaluation_status"] = i.evaluationstatus
        cohort_data["instructor_grade"] = i.instructorgrade
        cohort_data["evaluator_grade"] = i.evaluatorgrade
        cohort_data["project_comments"] = i.comments

        output.append(cohort_data)
    return jsonify({"output": output}), 200

@app.route('/api/delete_project/<id>', methods=['GET'])
def delete_project(id):
    project = ProjectTable.query.filter_by(id=id).first()
    print(project.id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted successfully"}), 200

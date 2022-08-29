from flask import jsonify
from api.services import *
from api import app
from api import db
from api.models import User, StudentTable, Cohorts, Bootcamp
from api.auth_routes import *
from api.scan_text_route import *
from api.studentRoutes import *
from api.advisor_sheet_routes import * 
from api.certificateRoutes import *
from api.attendanceRoutes import *


def insert_initial_values(*args, **kwargs):
    cohort1 = Cohorts(cohort=1)
    cohort2 = Cohorts(cohort=2)
    cohort3 = Cohorts(cohort=3)
    # bootcamp1 = Bootcamp(name="UI/UX", section=0, cohort_id=1)
    # bootcamp2 = Bootcamp(name="Web&Dev", section=0, cohort_id=1)
    # bootcamp3 = Bootcamp(name="DataScience", section=0, cohort_id=1)
    # student1 = StudentTable(gr="123456789", bootcamp_id=1, cohort_id=1)
    # db.session.add_all([cohort1, cohort2, cohort3, bootcamp1,
    #                    bootcamp2, bootcamp3, student1])
    db.session.add_all([cohort1, cohort2, cohort3])

    db.session.add(
        User(username='akhlaq.computer@gmail.com',
             public_id="ebb469cc-4cf6-4f3e-8bfb-1f642c3e20e5",
             password="sha256$pNWwKOrZpHpr7Vwm$dccc27c125def4d2ce0e915fca954d0d79a961557d3a34082815cdcf7399555d",
             admin=1))

    #password = abc12345
    db.session.add(
        User(username='umair.arif.m@gmail.com',
             public_id="8a0cc049-e8ae-4c19-9976-32be81bdbf91",
             password="sha256$tSgusbM9eEwastL8$b6bc1371cbc3fb75a36a3b0bb449231431da5e6a3b2ded6d64be2644e21c8a8d",
             admin=1))
    db.session.commit()


@app.route('/api/help', methods=['GET'])
def help():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)


# @app.after_request 
# def after_request(response):
#     header = response.headers
#     header['Access-Control-Allow-Origin'] = '*'
#     # Other headers can be added here if required
#     return response


if __name__ == '__main__':
    db.create_all()
    try:
        User.query.count()
    except:
        insert_initial_values(db)
        print("New Tables created")
    # app.run(debug=True, host="0.0.0.0", port=5000)
    app.run(debug=True, port=5000)
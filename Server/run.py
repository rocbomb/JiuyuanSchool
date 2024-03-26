from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship
from couse import CourseList
from student import students_data
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'
db = SQLAlchemy(app)

class StudyRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    study_time = db.Column(db.Integer, nullable=False)


@app.route('/api/study_records', methods=['POST'])
def create_study_record():
    student_id = request.json.get('student_id')
    course_id = request.json.get('course_id')
    study_time = request.json.get('study_time')
    study_record = StudyRecord(student_id=student_id, course_id=course_id, study_time=study_time)
    db.session.add(study_record)
    db.session.commit()
    return {'id': study_record.id}, 201

@app.route('/api/study_records', methods=['GET'])
def get_study_records():
    records = StudyRecord.query.all()
    return {'records': [{'id': r.id, 'student_id': r.student_id, 'course_id': r.course_id, 'study_time': str(r.study_time)} for r in records]}, 200


@app.route('/api/update_records', methods=['POST'])
def update_records():
    student_id = request.json.get('student_id')
    course_id = request.json.get('course_id')
    study_time = request.json.get('study_time')
    
    record = StudyRecord.query.filter_by(student_id = student_id, course_id = course_id).first()
    if record is None:
        record = StudyRecord(student_id = student_id, course_id = course_id, study_time = study_time)
        db.session.add(record)
        db.session.commit()
    else:
        record.study_time = record.study_time + study_time
        db.session.commit()
    return f"{course_id},{record.study_time}", 200

def findStudent(phone):
    for user in students_data:
        if str(user["phone"]) == str(phone):
            return user
    return None


@app.route('/api/login', methods=['POST'])
def login():
    userid = request.json.get('userid')
    password = request.json.get('password')

    student = findStudent(userid)

    if student is None:
        return {'id': "error", "error": "没有该用户"}, 201

    if str(student["password"]) != str(password):
        return {'id': "error", "error": "密码错误"}, 201

    records = StudyRecord.query.filter_by(student_id = student["id"]).all()

    videos = []
    for course in CourseList:
        if course["type"] in student["courses_list"]:
            videos.append(course)

    ret = {
        'id': student["id"],
        "name" : student["name"],
        "videos":videos,
        "records":[{'course_id': r.course_id, 'study_time': r.study_time} for r in records]
    }

    return ret, 201

def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db()
    app.run(debug=True, port=5000)

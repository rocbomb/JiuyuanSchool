from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship
from couse import CourseList
from student import students_data
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'
db = SQLAlchemy(app)
app.template_folder = os.path.join(os.getcwd(), 'html')

class StudyRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    study_time = db.Column(db.Integer, nullable=False)


@app.route('/api/result')
def studentInfos():
    all = request.args.get('pass')
    print(all)
    result = [
        {'name': '张三', 'course': '数学', 'over': "完成", 'study_time': '2'},
        {'name': '李四', 'course': '英语', 'over': "完成", 'study_time': '1.5'},
        {'name': '王五', 'course': '物理', 'over': "未完成", 'study_time': '3'}
    ]
    records = StudyRecord.query.all()
    for r in records:
        student_id = r.student_id
        course_id = r.course_id
        student_info = findStudentById(student_id)
        if student_info is None:
            continue
        course_info = findCourse(course_id)
        if course_info is None:
            continue
        over = "未完成"
        is_over = r.study_time / 60 + 1 > course_info['time']
        if is_over:
            over = "完成"
        info = {
            'name': student_info['name'],
            'course': course_info['name'],
            'over': over,
            'video_time': course_info['time'],
            'study_time': r.study_time / 60
            }
        if all == "false":
            result.append(info)
        elif is_over:
            result.append(info)
    return render_template('student.html', student_info=result)

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

def findStudentById(id):
    for user in students_data:
        if user["id"] == id:
            return user
    return None

def findCourse(id):
    for c in CourseList:
        if c["id"] == id:
            return c
    return None

@app.route('/api/login', methods=['POST'])
def login():
    userid = request.json.get('userid')
    password = request.json.get('password')

    student = findStudent(userid)

    if student is None:
        return {'id': -1, "error": "没有该用户"}, 201

    if str(student["password"]) != str(password):
        return {'id': -1, "error": "密码错误"}, 201

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

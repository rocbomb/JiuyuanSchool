from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    study_records = db.relationship('StudyRecord', backref='student')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    study_records = db.relationship('StudyRecord', backref='course')

class StudyRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    study_time = db.Column(db.Time, nullable=False)

#
@app.route('/init_student', methods=['GET'])
def init_student():
    with open("student.csv", 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            strs = line.split(',')
            if len(strs) < 3:
                continue
            _name = strs[0]
            _phone = strs[1]
            _password = strs[2]
            student = Student.query.filter_by(name=_name).first()
            if student is None:
                student = Student(name=_name, phone = _phone, password = _password)
                db.session.add(student)
                db.session.commit()
            elif student.phone !=_phone or student.password !=_password:
                student.phone =_phone
                student.password =_password
                db.session.commit()
    return {'message': "ok"}, 200

@app.route('/students', methods=['POST'])
def create_student():
    name = request.json.get('name')
    student = Student(name=name)
    db.session.add(student)
    db.session.commit()
    return {'id': student.id}, 201

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return {'students': [{'id': s.id, 'name': s.name} for s in students]}, 200

@app.route('/courses', methods=['POST'])
def create_course():
    name = request.json.get('name')
    course = Course(name=name)
    db.session.add(course)
    db.session.commit()
    return {'id': course.id}, 201

@app.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return {'courses': [{'id': c.id, 'name': c.name} for c in courses]}, 200

@app.route('/study_records', methods=['POST'])
def create_study_record():
    student_id = request.json.get('student_id')
    course_id = request.json.get('course_id')
    study_time = request.json.get('study_time')
    study_record = StudyRecord(student_id=student_id, course_id=course_id, study_time=study_time)
    db.session.add(study_record)
    db.session.commit()
    return {'id': study_record.id}, 201

@app.route('/study_records', methods=['GET'])
def get_study_records():
    records = StudyRecord.query.all()
    return {'records': [{'id': r.id, 'student_id': r.student_id, 'course_id': r.course_id, 'study_time': str(r.study_time)} for r in records]}, 200





@app.route('/login', methods=['GET'])
def login():
    userid = request.args.get('userid')
    password = request.args.get('password')

    student = Student.query.filter_by(phone=userid).first()

    if student is None:
        return {'id': -1, "error": "没有该用户"}, 201
    
    if student.password != str(password):
        return {'id': -1, "error": "密码错误"}, 201
    
    return {'id': student.id}, 201




def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db()
    app.run(debug=True)

import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request ,url_for
from flask import render_template, redirect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db = SQLAlchemy(app)
db.init_app(app)
app.app_context().push()


#models

#Student model describing student table and each columns of the table
class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    courses = db.relationship("Course",secondary="enrollments")

#Course model
class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code = db.Column(db.String, nullable=False, unique=True)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

#Enrollment model showing enrollment ids of students and courses
class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)


#homepage
@app.route('/',methods = ["GET"])
def index():
   if request.method == "GET":
       student = Student.query.all()
       print(student)
       return render_template("index.html",student=student)


#addstudent adds student and courses
@app.route('/student/create', methods = ["GET","POST"])
def addstudent():
    if request.method == "GET":
        return render_template("AddStudent.html")
    elif request.method == "POST":
        roll_number = request.form["roll"]
        first_name = request.form["f_name"]
        last_name = request.form["l_name"]
        stud = Student(roll_number=roll_number, first_name=first_name, last_name=last_name)
        db.session.add(stud)
        #db.session.commit()
        print(stud)
        courses = request.form.getlist('courses')
        print(courses)
        for course in courses:
            if course == 'course_1':
                stud.courses.append(Course.query.filter_by(course_id=1).one())
            if course == 'course_2':
                stud.courses.append(Course.query.filter_by(course_id=2).one())
            if course == 'course_3':
                stud.courses.append(Course.query.filter_by(course_id=3).one())
            if course == 'course_4':
                stud.courses.append(Course.query.filter_by(course_id=4).one())
        print(stud.courses)
        db.session.commit()
        return redirect('/')
    else:
        return redirect(url_for("index"))


# updates the student details using the student_id
@app.route('/student/<int:student_id>/update',methods = ["GET","POST"])
def update(student_id):
    if request.method == "GET":
        student = Student.query.get(student_id)
        return render_template("Update.html",student=student)
    if request.method == "POST":
        student = Student.query.get(student_id)
        roll_number=student.roll_number
        first_name = request.form["f_name"]
        last_name = request.form["l_name"]
        student.first_name=first_name
        student.last_name=last_name
        db.session.commit()
        #course_name = request.form["courses"]
        #addcourse = Course(course_name=course_name)
        #db.session.append(addcourse)
        #db.session.commit
        return redirect("/")
    return render_template("index.html")

#deletes the individual student and courses related to the student using the student_id
@app.route('/student/<int:student_id>/delete',methods =["GET","POST"])
def delete(student_id):
    if request.method == "GET":
        deleted= Student.query.get(student_id)
        db.session.delete(deleted)
        db.session.commit()
        return redirect("/")
        # else:
    return render_template("index.html")

#displays individual student details and courses related to the student  using the student_id
@app.route('/student/<int:student_id>',methods=["GET"])
def studentpage(student_id):
    if request.method == "GET":
        student = Student.query.get(student_id)
        return render_template("student page.html",student=student)
    else:
        return redirect('/')




#runs the app
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=8080)



from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SECRET_KEY'] = 'change-this-secret-key'
db = SQLAlchemy(app)

# ---------- Database Model ----------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(20), nullable=False, unique=True)
    course = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- Routes ----------
@app.route('/')
def index():
    query = request.args.get('q', '').strip()

    if query:
        students = Student.query.filter(
            (Student.name.ilike(f'%{query}%')) |
            (Student.roll_no.ilike(f'%{query}%')) |
            (Student.course.ilike(f'%{query}%'))
        ).order_by(Student.name).all()
    else:
        students = Student.query.order_by(Student.name).all()

    total_students = Student.query.count()
    total_courses = db.session.query(Student.course).distinct().count()

    return render_template(
        'index.html',
        students=students,
        title="Student List",
        query=query,
        total_students=total_students,
        total_courses=total_courses
    )

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name'].strip()
        roll_no = request.form['roll_no'].strip()
        course = request.form['course'].strip()
        email = request.form['email'].strip()

        existing = Student.query.filter_by(roll_no=roll_no).first()
        if existing:
            flash(f'Roll number "{roll_no}" already exists!', 'error')
            return render_template('form.html', title="Add Student", student=None)

        new_student = Student(name=name, roll_no=roll_no, course=course, email=email)
        db.session.add(new_student)
        db.session.commit()
        flash(f'{name} was added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('form.html', title="Add Student", student=None)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        student.name = request.form['name'].strip()
        student.roll_no = request.form['roll_no'].strip()
        student.course = request.form['course'].strip()
        student.email = request.form['email'].strip()
        db.session.commit()
        flash(f'{student.name} was updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('form.html', title="Edit Student", student=student)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    name = student.name
    db.session.delete(student)
    db.session.commit()
    flash(f'{name} was deleted.', 'success')
    return redirect(url_for('index'))

# ---------- Run ----------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

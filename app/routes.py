from flask import render_template, redirect, url_for, request, make_response
from datetime import datetime, timedelta
from app import app, db, celery, mail
from app.forms import StudentForm
from app.models import Student
import pdfkit
from flask_mail import Message


@app.route('/', methods=['GET', 'POST'])
def index():
    form = StudentForm()

    if request.method == 'GET':
        return render_template('student_form.html', form=form)

    try:
        if form.validate_on_submit():
            first_name = form.first_name.data
            second_name = form.second_name.data
            third_name = form.third_name.data
            personal_email = form.email.data
            course = form.course.data
            reg_number = form.reg_number.data

            student_by_regno = Student.query.filter_by(reg_number=reg_number).first()

            if student_by_regno:
                return "Student already exists"

            new_student = Student(first_name, second_name, third_name, personal_email, course, reg_number)
            db.session.add(new_student)
            db.session.commit()

            send_certificate.delay(new_student)

            return render_template('thankyou.html', student=new_student)
        else:
            return render_template('student_form.html', form=form)
    except:
        return "Error"

    return render_template('student_form.html', form=form)


@app.route('/admin', methods=['GET', 'PUT'])
def admin():
    filter_after = datetime.today() - timedelta(days=30)  # .filter(Student.created_at >= filter_after)
    apps_per_day = db.session.query(db.func.count(Student.id), db.func.strftime("%Y-%m-%d", Student.created_at)).\
        filter(Student.created_at >= filter_after) \
        .group_by(db.func.strftime("%Y-%m-%d", Student.created_at)).order_by(Student.created_at).all()
    certs_per_course = db.session.query(db.func.count(Student.id), Student.course).filter_by(email_sent=False) \
        .group_by(Student.course).order_by(Student.course) \
        .all()

    app_labels = [row[1] for row in apps_per_day]
    app_data = [row[0] for row in apps_per_day]
    cert_labels = [row[1] for row in certs_per_course]
    cert_data = [row[0] for row in certs_per_course]
    return render_template('dashboard.html', app_labels=app_labels, app_data=app_data, cert_labels=cert_labels,
                           cert_data=cert_data)


@celery.task(name='routes.send_certificate')
def send_certificate(student):
    # student = {'first_name': 'Adrian'}
    rendered = render_template('certificate.html', student=student)
    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
    options = {'enable-local-file-access': None}
    pdf = pdfkit.from_string(rendered, False, configuration=config, options=options)

    student_by_regno = Student.query.filter_by(reg_number=student.reg_number).first()

    msg = Message(f'Hi {student.first_name}', sender='', recipients=[student_by_regno.email])
    msg.attach("output.pdf", "application/pdf", pdf)
    mail.send(msg)

    student.email_sent = True
    db.session.commit()
    # response = make_response(pdf)
    # response.headers['Content-Type'] = 'application/pdf'
    # response.headers['Content-Disposition'] = 'inline; filename=output.pdf'


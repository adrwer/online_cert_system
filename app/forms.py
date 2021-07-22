from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email


class StudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    second_name = StringField('Second Name')
    third_name = StringField('Third Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    course = StringField('Course', validators=[InputRequired()])
    reg_number = StringField('Registration Number', validators=[InputRequired()])
    submit = SubmitField('Submit Information')

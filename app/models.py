from app import db
from datetime import datetime


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    second_name = db.Column(db.String(15))
    third_name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(15), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    reg_number = db.Column(db.String(50), nullable=False)
    email_sent = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, first_name, second_name, third_name, email, course, reg_number):
        self.first_name = first_name
        self.second_name = second_name
        self.third_name = third_name
        self.email = email
        self.course = course
        self.reg_number = reg_number

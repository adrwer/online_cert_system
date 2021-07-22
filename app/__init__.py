from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail_celery import make_celery
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '60b5651ded3ae4446d70649afb49556f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)
celery = make_celery(app)
mail = Mail(app)

from app import models, routes, forms

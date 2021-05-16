from src import db
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app as app
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy import *

# MODEL


class UserAccounts(UserMixin, db.Model):
    id = db.Column(db.Integer,    primary_key=True, autoincrement=True)
    name = db.Column(db.String(59),  nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)
    fb_link = db.Column(db.String(180), unique=True, nullable=True)
    address = db.Column(db.String(180), nullable=True)
    contact_person = db.Column(db.String(180), nullable=True)
    contact_person_number = db.Column(db.String(20), nullable=True)
    previous_school = db.Column(db.String(180), nullable=True)
    incoming_school = db.Column(db.String(180), nullable=True)
    incoming_grade_level = db.Column(db.String(180),  nullable=True)
    course = db.Column(db.String(180),  nullable=True)
    package = db.Column(db.String(180),  nullable=True)
    barkada_name = db.Column(db.String(59))
    schedule = db.Column(db.String(180),  nullable=True)
    payment_method = db.Column(db.String(180),  nullable=True)
    promo_code = db.Column(db.String(59))
    barkada_name = db.Column(db.String(59))
    internet_speed = db.Column(db.String(59))
    concerns = db.Column(db.String(180))
    is_admin = db.Column(db.Boolean, default=False)

class UpgradeTutors(UserMixin, db.Model):
    id = db.Column(db.Integer,    primary_key=True, autoincrement=True)
    name = db.Column(db.String(59),  nullable=False)
    current_school = db.Column(db.String(59),  nullable=False)
    year_and_degree_program = db.Column(db.String(59),  nullable=False)
    high_school = db.Column(db.String(59),  nullable=False)
    grade = db.Column(db.String(59),  nullable=False)
    awards_hs = db.Column(ARRAY(String), nullable=False, default={})
    awards_college = db.Column(ARRAY(String), nullable=False, default={})
    num_of_referrals = db.Column(db.Integer, nullable=False)
    text_id = db.Column(db.String(59),  nullable=False)

class tutors_promo_code(UserMixin, db.Model):
    id = db.Column(db.Integer,    primary_key=True, autoincrement=True)
    tutors = db.Column(db.String(59),  nullable=False)
    promo_code = db.Column(db.String(59),  nullable=False)
    num_referrals = db.Column(db.Integer, nullable=False)





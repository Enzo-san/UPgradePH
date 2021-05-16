from flask import Blueprint, render_template, redirect, url_for, flash
from flask.globals import session
from src.user.models import *
#from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from .models import UserAccounts, tutors_promo_code
from .forms import RegisterFormPage1, RegisterFormPage2, RegisterFormPage3
from src import bcrypt
from src import login_manager
from src import db
import random, string
from flask import Flask, render_template, request
from sqlalchemy import func
#from .models import UserAccounts

import smtplib
#import pandas as pd 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

# Set up a Blueprint
upgrade_blueprint = Blueprint('upgrade_blueprint', __name__)


@upgrade_blueprint.route('/')
def index():
	return render_template('home.html')


@upgrade_blueprint.route('/BasicAccounting')
def BasicAccounting():
	
	return render_template('basic-acc.html')


@upgrade_blueprint.route('/Precalculus')
def Precalculus():
	return render_template('precalculus.html')


@upgrade_blueprint.route('/Calculus')
def Calculus():
	return render_template('calculus.html')


@upgrade_blueprint.route('/Physics')
def Physics():
	return render_template('intro-physics.html')

@upgrade_blueprint.route('/Sitemap')
def sitemap():
	return render_template('sitemap.xml')


@upgrade_blueprint.route('/Register', methods=['GET', 'POST'])
def register1():
	form = RegisterFormPage1()
	if form.validate_on_submit():
		session['name'] = form.name.data
		session['email'] = form.email.data
		session['phone_number'] = form.phone_number.data
		session['fb_link'] = form.fb_link.data
		session['address'] = form.address.data
		session['contact_person'] = form.contact_person.data
		session['contact_person_number'] = form.contact_person_number.data
		# new_user = UserAccounts(
		# 	name            				= form.name.data, 
		# 	email           				= form.email.data,
		# 	phone_number    				= form.phone_number.data,
		# 	fb_link         				= form.fb_link.data,
		# 	address         				= form.address.data,
		# 	contact_person  				= form.contact_person.data,
		# 	contact_person_number   		= form.contact_person_number.data)
		# db.session.add(new_user)
		# db.session.commit()
		return redirect(url_for('upgrade_blueprint.register2'))
	return render_template('reg-step1.html', form=form)


@upgrade_blueprint.route('/Register2', methods=['GET', 'POST'])
def register2():
	form = RegisterFormPage2()
	if form.validate_on_submit():
		session['previous_school'] = form.previous_school.data
		session['incoming_school'] = form.incoming_school.data
		session['incoming_grade_level'] = form.incoming_grade_level.data
		session['course'] = form.course.data
		# new_user = UserAccounts(
		# 	previous_school            		= form.previous_school.data, 
		# 	incoming_school           		= form.incoming_school.data,
		# 	incoming_grade_level    		= form.incoming_grade_level.data,
		# 	course         					= form.course.data)
		# db.session.add(new_user)
		# db.session.commit()
		return redirect(url_for('upgrade_blueprint.register3'))
	return render_template('reg-step2.html', form=form)


@upgrade_blueprint.route('/Register3', methods=['GET', 'POST'])
def register3():
	promo_codes = tutors_promo_code.query.with_entities(tutors_promo_code.promo_code).all()
	package_list = {
		'Basic Accounting 1-on-1' : 11000,
		'Basic Accounting 1-on-3' : 8500,
		'Basic Accounting 1-on-5' : 7500,
		'Precalculus 1-on-1' : 11000,
		'Precalculus 1-on-3' : 8500,
		'Precalculus 1-on-5' : 7500,
		'Differential Calculus 1-on-1' : 11000,
		'Differential Calculus 1-on-3' : 8500,
		'Differential Calculus 1-on-5' : 7500,
		'Introductory Physics 1-on-1' : 12000,
		'Introductory Physics 1-on-3' : 9500,
		'Introductory Physics 1-on-5' : 8500,
	}

	form = RegisterFormPage3()
	if form.validate_on_submit():
		session['package'] = form.package.data
		session['barkada_name'] = form.barkada_name.data
		session['schedule'] = form.schedule.data
		session['payment_method'] = form.payment_method.data
		session['promo_code'] = form.promo_code.data
		session['internet_speed'] = form.internet_speed.data
		session['concerns'] = form.concerns.data

		new_user = UserAccounts(
			name            				= session['name'], 
			email           				= session['email'],
			phone_number    				= session['phone_number'],
			fb_link         				= session['fb_link'],
			address         				= session['address'],
			contact_person  				= session['contact_person'],
			contact_person_number   		= session['contact_person_number'],
			previous_school            		= session['previous_school'], 
			incoming_school           		= session['incoming_school'],
			incoming_grade_level    		= session['incoming_grade_level'],
			course         					= session['course'],
			package            				= session['package'],
			barkada_name           			= session['barkada_name'],
			schedule    					= session['schedule'],
			payment_method         			= session['payment_method'],
			promo_code    					= session['promo_code'],
			internet_speed    				= session['internet_speed'],
			concerns    					= session['concerns'])
		db.session.add(new_user)
		db.session.commit()

		amount_to_pay = package_list.get(session['package'])
		valid_promo_code = False

		records = tutors_promo_code.query.filter(tutors_promo_code.promo_code==session['promo_code']).all()
		for temp in records:
			referrals = temp.num_referrals
			referrals += 1
			temp.num_referrals = referrals
			valid_promo_code = True
			db.session.commit()

		if valid_promo_code:
			amount_to_pay -= 500

		sendPaymentDetails(session['name'], session['email'], session['payment_method'], session['promo_code'], session['package'], amount_to_pay)
		return redirect(url_for('upgrade_blueprint.register_success'))
	
	return render_template('reg-step3.html', form=form, promo_codes=promo_codes)

@upgrade_blueprint.route('/Register-Sucess')
def register_success():
	return render_template('register-success.html')


def sendPaymentDetails(name, email, payment_method, promo_code, package, amount_to_pay):
    msg = MIMEMultipart()
    fromaddr = "admin@upgradetutorials.ph"
    toaddr = email
    s = smtplib.SMTP_SSL('mail.privateemail.com', 465) 
    s.set_debuglevel(1) 
    s.login(fromaddr, "AdminUpgrade120719")
    msg['From'] = fromaddr 
    msg['To'] = toaddr
    msg['Subject'] = "Upgrade College Preparation Tutorials Payment Details"

    body = "Dear " + name + ", \n\n\n \
	Thank you for choosing to kickstart your college journey with us! In order to officially reserve your slot, please pay Php " + str(amount_to_pay) + " to either our official bank account or Gcash account. \n \
	The account details are listed below. \n\n \
	\tBank account (UnionBank) \n \
	\t\t Account number: 0001 3001 9756 \n \
	\t\t Account name: UPGRADEPH TUTORIAL SERVICES \n\n \
	\tGcash account \n \
	\t\t Account number: 0947 880 7109 \n \
	\t\t Account name: Eduardo Maurice Fiel \n\n \
	Please take note that your slot will only be reserved once paid. After paying, please take the following steps: \n \
	\t 1. Take a photo or screenshot of your proof of payment. \n \
	\t 2. Reply to this email with attached photo or screenshot of your proof of payment. \n \
    \t\t 3. We will reply to your e-mail once we have verified your payment. \n\n \
	Should you have any problems or concerns, please do not hesitate to reply to this e-mail or contact us via our contact numbers listed below. \n\n\n \
	We are excited to work with you and thank you again for choosing to UPgrade! \n"


    msg.attach(MIMEText(body, 'plain')) 
	
    # # filename = "email-signature.png"
    # # attachment = open("src/static/img/email-signature.png", "rb")
    # # p = MIMEBase('application', 'octet-stream') 
    
    # msg.attach(MIMEText(body +
	# '<p><img src="src/static/img/email-signature.png"></p>' +
	# '</body></html>', 'html', 'utf-8'))

    # # p.set_payload((attachment).read()) 
    
    # # encoders.encode_base64(p) 
    
    # # p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    

    # # msg.attach(p) 
    text = msg.as_string() 
    s.sendmail(fromaddr, toaddr, text)
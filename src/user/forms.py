from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField
from wtforms.fields.core import SelectField
from wtforms.validators import InputRequired, Email, Length,DataRequired, EqualTo, ValidationError
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from .models import UserAccounts as UserAccounts
from src import login_manager
#from flask.ext.wtf import Form
from wtforms import validators
from wtforms.fields.html5 import EmailField

class RegisterFormPage1(FlaskForm):
    name = StringField('Full Name', validators=[InputRequired(), Length(min=4, max=59)])
    email = EmailField('Email', validators=[InputRequired(), Length(min=4, max=50)])
    phone_number = StringField('Phone Number', validators=[InputRequired(), Length(min=11, max=11)])
    fb_link = StringField('Facebook Account Link', validators=[InputRequired(), Length(min=4, max=180)])
    address = StringField('City Address', validators=[InputRequired(), Length(min=4, max=50)])
    contact_person = StringField('Contact Person for Emergency', validators=[InputRequired(), Length(min=4, max=180)])
    contact_person_number = StringField('Emergency Contact Person Number', validators=[InputRequired(), Length(min=11, max=11)])

class RegisterFormPage2(FlaskForm):
    previous_school = StringField('Previous School', validators=[InputRequired(), Length(min=2, max=180)])
    incoming_school = StringField('Incoming School', validators=[InputRequired(), Length(min=2, max=180)])
    incoming_grade_level = SelectField('Incoming Grade Level', choices=[
                                                                        ('Grade 7','Grade 7'), 
                                                                        ('Grade 8','Grade 8'), 
                                                                        ('Grade 9','Grade 9'), 
                                                                        ('Grade 10','Grade 10'), 
                                                                        ('Grade 11','Grade 11'), 
                                                                        ('Grade 12','Grade 12'),
                                                                        ('First Year','First Year College'), 
                                                                        ('Second Year','Second Year College'), 
                                                                        ('Third Year','Third Year College')
                                                                        ], 
                                                                        validators=[InputRequired()]
                                      )
    course = StringField('Course/Academic Strand', validators=[InputRequired(), Length(min=4, max=180)])

class RegisterFormPage3(FlaskForm):
    package = SelectField('Package', choices=[
                                                ('','Select Package Type'), 
                                                ('Basic Accounting 1-on-1','Basic Accounting 1-on-1'), 
                                                ('Basic Accounting 1-on-3','Basic Accounting 1-on-3'), 
                                                ('Basic Accounting 1-on-5','Basic Accounting 1-on-5'), 
                                                ('Precalculus 1-on-1','Precalculus 1-on-1'), 
                                                ('Precalculus 1-on-3','Precalculus 1-on-3'), 
                                                ('Precalculus 1-on-5','Precalculus 1-on-5'),
                                                ('Differential Calculus 1-on-1','Differential Calculus 1-on-1'), 
                                                ('Differential Calculus 1-on-3','Differential Calculus 1-on-3'), 
                                                ('Differential Calculus 1-on-5','Differential Calculus 1-on-5'),
                                                ('Introductory Physics 1-on-1','Introductory Physics 1-on-1'), 
                                                ('Introductory Physics 1-on-3','Introductory Physics 1-on-3'), 
                                                ('Introductory Physics 1-on-5','Introductory Physics 1-on-5')
                                                ]]
                         )
    barkada_name = StringField('Name of Other People Included in Barkada', validators=[Length(min=4, max=180)], render_kw={"placeholder": "Ex. Juan C. dela Cruz, Maria C. dela Cruz, Juana C. dela Cruz"})
    schedule = SelectField('Incoming Grade Level', choices=[
                                                            ('','Select a schedule'), 
                                                            ('MWF 8:00 am - 10:00 am','MWF 8:00 am - 10:00 am'), 
                                                            ('MWF 10:00 am - 12:00 nn','MWF 10:00 am - 12:00 nn'), 
                                                            ('MWF 1:00 pm - 3:00 pm','MWF 1:00 pm - 3:00 pm'), 
                                                            ('MWF 3:00 pm - 5:00 pm','MWF 3:00 pm - 5:00 pm'), 
                                                            ('TThS 8:00 am - 10:00 am','TThS 8:00 am - 10:00 am'), 
                                                            ('TThS 10:00 am - 12:00 nn','TThS 10:00 am - 12:00 nn'),
                                                            ('TThS 1:00 pm - 3:00 pm','TThS 1:00 pm - 3:00 pm'), 
                                                            ('TThS 3:00 pm - 5:00 pm','TThS 3:00 pm - 5:00 pm')
                                                            ], 
                                                            validators=[InputRequired()]
                          )
    payment_method = SelectField('Preferred Payment Method', choices=[
                                                            ('','Select payment method'), 
                                                            ('GCash','GCash'), 
                                                            ('Bank Transfer','Bank Transfer')
                                                            ], 
                                                            validators=[InputRequired()]
                          )
    promo_code = StringField('Promo Code', validators=[Length(min=3, max=180)], render_kw={"placeholder": "Type N/A if not applicable"})
    internet_speed = StringField('Internet Speed (in mbps)', validators=[InputRequired(), Length(min=1, max=180)])
    concerns = StringField('Other Concerns?')
import flask_wtf
import wtforms
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import DecimalField, StringField, DateTimeField, IntegerField, RadioField, SubmitField, validators, Form
from wtforms.validators import Length, DataRequired






class NewCustomerForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField('Full Name' , validators = [validators.DataRequired(), validators.Length(min=5, max=50, message="Name must be between 5 and 50 Characters")])
    dob = StringField('Date of Birth MM/DD/YYYY' , validators = [validators.DataRequired(), validators.Length(min=10, max=10, message="DD/MM/YYYY")])
    ssn = StringField('Social Security Number' , validators = [validators.DataRequired(), validators.Length(min=9, max=9, message="SSN is 9 Digits")])
    submit = SubmitField('Submit')

class NewAccountForm(FlaskForm):
    class Meta:
        csrf = False


    products = [("1","Regular Non-Personal"),("2", "Personal Account"),("3", "High Interest Checking"),("4","Savings Account")]
    account_number = IntegerField('Account Number', [validators.DataRequired() ])
    primary_ssn = StringField('Social Security Number' , [validators.DataRequired(), validators.Length(min=9,max=9,message="SSNs are 9 Digits") ])
    bal = DecimalField('Opening Deposit', [validators.DataRequired() ])
    product = RadioField('Product', [validators.DataRequired()], choices=products)
    submit = SubmitField('Submit')


class CustomerForm(FlaskForm):
    class Meta:
        cstf = False
        
    primary_ssn = StringField('Social Security Number' , [validators.DataRequired(), validators.Length(min=9,max=9,message="SSNs are 9 Digits") ])


    

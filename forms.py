import flask_wtf
import wtforms
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import DecimalField, StringField, DateTimeField, IntegerField, RadioField, SubmitField, validators, Form, SelectField
from wtforms.validators import Length, DataRequired


#TODO finish setting up form for Teller Login

class TellerLoginForm(FlaskForm):       
    class Meta:
        csrf = False
    
    teller_id = IntegerField('Teller ID')
    submit = SubmitField('Submit')



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


    products = [("Regular Non-Personal","Regular Non-Personal"),("Personal Account", "Personal Account"),("High Interest Checking", "High Interest Checking"),("Savings Account","Savings Account")]
    account_number = IntegerField('Account Number', [validators.DataRequired() ])
    primary_ssn = StringField('Social Security Number' , [validators.DataRequired(), validators.Length(min=9,max=9,message="SSNs are 9 Digits") ])
    bal = DecimalField('Opening Deposit', [validators.DataRequired() ])
    product = RadioField('Product', [validators.DataRequired()], choices=products)
    submit = SubmitField('Submit')


class CustomerForm(FlaskForm):
    class Meta:
        csrf = False        #TODO make a dynamic field to add multiple customers to an account at a time.
    account = IntegerField('Account Number', [validators.DataRequired()])
    new_ssn = StringField('Social Security Number' , [validators.DataRequired(), validators.Length(min=9,max=9,message="SSNs are 9 Digits") ])
    submit = SubmitField('Add Customer')

'''
class NumberOfCustomers(Form):
    class Meta:
        csrf = False

    number_of_customers = IntegerField('Number of customers to add to account', [validators.DataRequired(), validators.NumberRange(0,10)])

'''
class TellerBuyForm(FlaskForm):
    class Meta:
        csrf = False
    
    #Set session Teller ID to ID for Teller, This will be the same for all transaction Forms.
    buy_from_id = IntegerField('Who did you buy from?', [validators.DataRequired()]) #TODO make range only allow for teller IDs that exist.
    amount = DecimalField('Amount', [validators.DataRequired() ])
    description = StringField('Comments', [validators.DataRequired(), validators.Length(max=100)])
    submit = SubmitField('Submit')

class TellerSellForm(FlaskForm):
    class Meta:
        csrf = False
    
    sell_to_id = IntegerField('Who did you sell to?', [validators.DataRequired()]) #TODO make range only allow for teller IDs that exist.
    amount = DecimalField('Amount', [validators.DataRequired()])
    description = StringField('Comments', [validators.DataRequired(), validators.Length(max=100)])
    submit = SubmitField('Submit')

class DepositForm(FlaskForm):
    class Meta:
        csrf = False
    
    account = IntegerField('Account Number', [validators.DataRequired()])
    amount = DecimalField('Amount of Deposit', [validators.DataRequired()])
    submit = SubmitField('Submit')
    

class WithdrawlForm(FlaskForm):
    class Meta:
        csrf = False
    
    account = IntegerField('Account Number', [validators.DataRequired()])
    amount = DecimalField('Amount of Withdrwl', [validators.DataRequired()])
    submit = SubmitField('Submit')

class InquiryForm(FlaskForm):
    class Meta:
        csrf = False
    
    account_number = IntegerField('Account Number' , validators = [validators.DataRequired()])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    class Meta:
        csrf = False
    search_type = RadioField('Type', validators = [validators.DataRequired()], choices=[('customer','Customer'), ('account', 'Account')],)
    attr_type = SelectField('Search Parameter', choices = [], validators = [validators.DataRequired()])
    search_param = StringField('Search For', validators = [validators.DataRequired()])
    
    submit = SubmitField('Submit')

class TransferForm(FlaskForm):
    class Meta:
        csrf = False
    
    debit_account = IntegerField('Debit Account Number', [validators.DataRequired()])
    credit_account = IntegerField('Credit Account Number', [validators.DataRequired()])

    amount = DecimalField('Amount of Transfer', [validators.DataRequired()])

    submit = SubmitField('Submit')

class BalanceForm(FlaskForm):
    class Meta:
        csrf = False

    hundreds = IntegerField('Hundreds', [validators.DataRequired()])
    fifties = IntegerField('Fifties', [validators.DataRequired()])
    twenties = IntegerField('Twenties', [validators.DataRequired()])
    tens = IntegerField('Tens', [validators.DataRequired()])
    fives = IntegerField('Fives', [validators.DataRequired()])
    twos = IntegerField('Twos', [validators.DataRequired()])
    ones = IntegerField('Ones', [validators.DataRequired()])
    dollarc = IntegerField('Dollar Coins', [validators.DataRequired()])
    halves = IntegerField('Halves', [validators.DataRequired()])
    quarters = IntegerField('Quarters', [validators.DataRequired()])
    dimes = IntegerField('Dimes', [validators.DataRequired()])
    nickels = IntegerField('Nickels', [validators.DataRequired()])
    pennies = IntegerField('Pennies', [validators.DataRequired()])



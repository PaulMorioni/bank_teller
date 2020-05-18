from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import *
import random
import re
from forms import NewCustomerForm, NewAccountForm, DepositForm


__name__ = '__main__'
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bank_teller:bankandtrust@localhost:8889/bank_teller'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337ksdfwh34132w'


#TODO Add a teller class to do teller functions through?? What should be done with buy/sell cash if not. (I.e. only effects Vault(maybe) and teller GL)

class Teller(db.Model):

    teller_id = db.Column(db.Integer, primary_key=True)
    cashbal = db.Column(db.Numeric(18,4))
    cashdenom = db.Column(db.String(20))

    def __init__(self, cashbal, cashdenom):
        self.cashbal = 0
        self.cashdenom = [0,0,0,0,0,0,0,0,0,0,0,0,0]

'''
    def balance():
        done = False
        hundreds = 0 # pull input from UI #TODO
        fifties = 0
        twenties = 0
        tens = 0
        fives = 0
        twos = 0
        ones = 0
        dollarc = 0
        halves = 0
        quarters = 0
        dimes = 0
        nickels = 0
        penies = 0

        while done == False:
    

    def changecash(trancode, amount):  #TODO
        cur_cash = self.cashbal

    Any transaction types should actually be held in this module and should only be tied to the account module with
    With the tran attribute of account number
    
    @staticmethod
    def deposit(account_number, check_amount, cash_amount, cashback, total):
        if total == check_amount + cash_amount - cashback:
            current_account = Account.search_account(account_number, account_number, all_accounts) #TODO does all_accounts work this way or will i need to change the startup() function
            current_balance = current_account.balance
            new_balance = current_balance + total
            current_account.balance = new_balance
   '''
accounts_owners = db.Table('accounts_owners',
    db.Column('account_id', db.Integer, db.ForeignKey('account.account_id')),
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.customer_id'))
)  

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dob = db.Column(db.String(30))
    ssn = db.Column(db.Integer, unique=True)
    accounts = db.relationship("Account", secondary=accounts_owners, lazy='subquery', 
        backref=db.backref("customer", lazy=True))
    
    def __init__(self, ssn, name, dob):
        self.ssn = ssn
        self.name = name
        self.dob = dob

    def parse_name(self):
        full_name = str(self.name)
        parsed_name = full_name.split(' ')
        return parsed_name

    def formatted_string_ssn(self):
        str_ssn = str(self.ssn)
        block1 = str_ssn[0:3]
        block2 = str_ssn[3:5]
        block3 = str_ssn[5:9]
        formated_ssn = block1 + "-" + block2 + "-" + block3
        return formated_ssn


class Account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True)
    acctn = db.Column(db.Integer, unique=True)
    primary_ssn = db.Column(db.Integer)
    prod = db.Column(db.String(50))
    date_opened = db.Column(db.String(25))
    bal = db.Column(db.Numeric(18,4))
    transactions = db.relationship('Trans', backref='account', lazy='dynamic')
    
    def __init__(self, primary_ssn, acctn, bal, prod, date_opened):
        self.primary_ssn = primary_ssn
        self.acctn = acctn
        self.bal = bal
        self.prod = prod
        self.date_opened = date_opened

    def calc_balance(self, trancode, amount):
    
        current_balance = self.bal
        if trancode in (13, 113, 400):
            new_balance = current_balance + amount
            self.bal = new_balance
            db.session.commit()
        
        elif trancode in (50, 500, 150):
            new_balance = current_balance - amount
            self.bal = new_balance
            db.session.commit()


        


class Trans(db.Model):
    tran_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(25))
    amount = db.Column(db.Numeric(18,4))
    description = db.Column(db.String(100))
    trancode = db.Column(db.Integer)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'))

    def __init__(self, tran_time, amount, description, trancode):
        self.time = tran_time
        self.amount = amount
        self.description = description
        self.trancode = trancode

    def rounded_amount(self):
        rounded_amount = round(self.amount, 2)
        return rounded_amount

    def time_datetime(self):
            str_tran_date = self.time
            tran_datetime = datetime.strptime(str_tran_date,'%x , %X')
            return tran_datetime




@app.route('/', methods = ['POST', 'GET'])
def base():
    title = "Test 1"
    account_readout = True

    accounts = Account.query.all()
    customers = Customer.query.all()


    return render_template("base.html", title=title, account_readout=account_readout, accounts=accounts, customers=customers)


@app.route('/home', methods = ['POST', 'GET'])
def home():
    

    return render_template()


@app.route('/deposit', methods = ['POST', 'GET'])
def deposit():
    form = DepositForm()
    trancode = 13

    if request.method == 'GET':
        
        return render_template('deposit.html', account_readout = False, form=form)

    else:
        account_number = form.account.data

        account = Account.query.filter_by(acctn=account_number).first()

        amount = form.amount.data

        desc = 'Deposit with Teller'
        tran_time = datetime.now()
        str_tran_time = tran_time.strftime('%x , %X')

        new_deposit = Trans(str_tran_time, amount, desc, trancode)

        account.transactions.append(new_deposit)

        db.session.add(new_deposit)
        account.calc_balance(trancode, amount)
        db.session.commit()

        return render_template('success.html' )


@app.route('/withdrawl', methods = ['POST', 'GET'])
def withdrawl():


    return render_template()

@app.route('/transfer', methods = ['POST', 'GET'])
def transfer():

    
    return render_template()


@app.route('/inquiry', methods = ['POST', 'GET'])
def inquiry():
    customer = Customer.query.filter_by(ssn='123456789').first()
    accounts = customer.accounts
    for account in accounts:
        account.sort_tran_by_date()
    
    return render_template('inquiry.html', account_readout=True, customer=customer, accounts=accounts)


@app.route('/balance', methods = ['POST', 'GET'])
def balance():


    return render_template()


@app.route('/buy', methods = ['POST', 'GET'])
def buy():


    return render_template()


@app.route('/sell', methods = ['POST', 'GET'])
def sell():


    return render_template()

@app.route('/new_account', methods = ['POST', 'GET'])
def make_account():
    form = NewAccountForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('new_account.html', account_readout=False, form=form)
        else:

            account_number = form.account_number.data
            primary_ssn = form.primary_ssn.data
            opening_deposit =form.bal.data
            product = form.product.data
            date_opened = datetime.now()
            str_date_opened = date_opened.strftime("%x")    

            customer = Customer.query.filter_by(ssn=primary_ssn).first()
            if customer:        #TODO most likely change this to a catch error
                owner_ssn = customer.ssn
                account = Account(owner_ssn, account_number, opening_deposit, product, str_date_opened)

                customer.accounts.append(account)       #Relates customer to account owner.

                db.session.add(account)
                db.session.commit()
                return render_template('success.html', title="Success")
            else:
                error = "Customer Does not Exist"
                return render_template('new_account.html', error=error, account_readout=False, form=form)
            

    if request.method == 'GET':
        return render_template('new_account.html', account_readout=False, form=form)


@app.route('/new_customer', methods = ['POST', 'GET'])
def make_customer():
    form = NewCustomerForm(request.form)

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('new_customer.html', account_readout=False, form=form)
        if form.validate():
            name = form.name.data
            dob = form.dob.data
            ssn = form.ssn.data
            customer = Customer(ssn, name, dob)
            db.session.add(customer)
            db.session.commit()

            return render_template('success.html', title="Success")

    if request.method == 'GET':
        return render_template('new_customer.html', account_readout=False, form=form)


if __name__ == '__main__':

    app.run()

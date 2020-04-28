from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import datetime
import random
import generator
import re

__name__ = '__main__'
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bank_teller:bankandtrust@localhost:8889/bank_teller'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337ksdfwh34132w'


#TODO Add a teller class to do teller functions through?? What should be done with buy/sell cash if not. (I.e. only effects Vault(maybe) and teller GL)
'''
class Teller(db.Model):

    
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, cashbal, cashdenom):
        self.cashbal = 0
        self.cashdenom = [0,0,0,0,0,0,0,0,0,0,0,0,0]

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
    db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.id')) 
)  

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dob = db.Column(db.Integer)
    ssn = db.Column(db.Integer, unique=True)
    accounts = db.relationship("Account", secondary=accounts_owners, lazy='subquery', 
        backref=db.backref("customer", lazy=True))
    
    def __init__(self, ssn, name, dob):
        self.ssn = ssn
        self.name = name
        self.dob = dob

    '''def str_id(self):
        cust_id = self.id
        str_id = str(cust_id)
        return  str_id

    def str_ssn(self):
        ssn = self.ssn
        str_ssn = str(ssn)
        return str_ssn

    def str_dob(self):
        dob = self.dob
        str_dob = str(dob)
        return str_dob

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

    @staticmethod
    def make_customer():

        cust_id = input('Enter ID Number: ')
        ssn = input('Enter SSN: ')
        name = input('Enter Full Name: ')
        dob = input('Enter Date of Birth:')
        new_customer = Customer(cust_id, ssn, name, dob)
        Customer.store(new_customer)
        return new_customer

'''

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acctn = db.Column(db.Integer, unique=True)
    prod = db.Column(db.String(50))
    date_opened = db.Column(db.String(25))  #Owners should be stored in Account class as Account.customer?
    transactions = db.relationship('Trans', backref='account', lazy='dynamic')
    
    #TODO Need to set foreign keys for join table with customer ssn
    def __init__(self, owner_ids, acctn, bal, prod, date_opened):
                                        #Join with Customer DB via SSN #TODO
        self.acctn = acctn
        self.prod = prod
        self.date_opened = date_opened
        self.owner_ids = owner_ids
        self.bal = bal

        #Store the parameter translist to easily do a query on all transactions associated with an account
                                        # #Join with Trans DB to call for specific Account number #TODO


'''
    @staticmethod
    def make_account():
        owner_ids = []
        acctn = input('Enter Account Number: ')
        number_of_owners = int(input('Enter Number of Account Owners: '))
        for i in range(0,number_of_owners):
            print(i)
            ssn = input('Enter SSN: ')
            owner_ids.append(ssn)
        starting_balance = input('Enter Amount of Initial Deposit: ')
        prod = input('Enter Product Name: ')
        date_opened = datetime.now()
        new_acct = Account(owner_ids,acctn, starting_balance, prod, date_opened)
        Account.store(new_acct)
        return new_acct

'''




class Trans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    amount = db.Column(db.String(50))
    description = db.Column(db.String(100))
    trancode = db.Column(db.Integer)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __init__(self, id : int, tran_time : datetime, amount : float, description : str, trancode: int):
        self.id = id
        self.time = tran_time
        self.amount = amount
        self.description = description
        self.trancode = trancode 
'''
    @staticmethod
    def make_transaction():
        tran_id = int(input('Enter ID Number: '))
        account_number = input('Enter Account Number: ')
        amount = float(input('Enter Amount: '))
        description = input('Enter Description: ')
        trancode = int(input('Enter Trancode: '))
        tran_time = datetime.now()
        new_transaction = Trans(tran_id, tran_time, amount, description, trancode, account_number)
        Trans.store(new_transaction)
        return new_transaction
'''

'''
def generate_data():
    cust_amount = input('Enter Number of Customers: ')
    acct_amount = input('Enter Number of Accounts: ')
    trans_amount = input('Enter Number of Transactions: ')
    months = input('Enter How Many Months of Data:')
    customer_list, account_list, trans_list = generator.generate(cust_amount, acct_amount, trans_amount, months)
    new_Customer_list = []  #List of instantiated customer objects from generator data
    new_Account_list = []
    new_Trans_list = []

    for customer in customer_list:
        dob = customer.pop()
        name = customer.pop()
        ssn = customer.pop()
        id = customer.pop()
        new_Customer = Customer(id, ssn, name, dob)
        new_Customer_list.append(new_Customer)
        Customer.store(new_Customer)

    for account in account_list:
        owner_ssn = account.pop()
        date_opened = account.pop()
        prod = account.pop()
        bal = account.pop()
        acct_number = account.pop()
        new_Account = Account(owner_ssn, acct_number, bal, prod, date_opened)
        new_Account_list.append(new_Account)
        Account.store(new_Account)

    for transaction in trans_list:
        accountn = transaction.pop()        #Pops in reverse order of the instantiation of a trans object
        tran_balance = transaction.pop()
        desc = transaction.pop()
        trancode = transaction.pop()
        tran_time = transaction.pop()
        tran_id = transaction.pop()
        new_Tran = Trans(tran_id, tran_time, tran_balance, desc, trancode, accountn)
        new_Trans_list.append(new_Tran)
        Trans.store(new_Tran)

    return new_Customer_list, new_Account_list, new_Trans_list



def startup():

    all_customers = Customer.import_customers()
    all_accounts = Account.import_accounts()
    all_trans = Trans.import_trans()
    return all_customers, all_accounts, all_trans

'''
#def main():



@app.route('/', methods = ['POST', 'GET'])
def base():
    title = "Test 1"
    account_readout = True

    accounts = Account.query.all()
    customers = Customer.query.all()


    return render_template("base.html", title=title, account_readout=account_readout, accounts=accounts, customers=customers)

'''
@app.route('/home', methods = ['POST', 'GET'])
def home():
    

    return render_template()


@app.route('/deposit', methods = ['POST', 'GET'])
def deposit():

    
    return render_template()


@app.route('/withdrawl', methods = ['POST', 'GET'])
def withdrawl():


    return render_template()

@app.route('/transfer', methods = ['POST', 'GET'])
def transfer():

    
    return render_template()


@app.route('/inquiry', methods = ['POST', 'GET'])
def inquiry():


    return render_template()


@app.route('/balance', methods = ['POST', 'GET'])
def balance():


    return render_template()


@app.route('/buy', methods = ['POST', 'GET'])
def buy():


    return render_template()


@app.route('/sell', methods = ['POST', 'GET'])
def sell():


    return render_template()
'''

if __name__ == '__main__':

    app.run()

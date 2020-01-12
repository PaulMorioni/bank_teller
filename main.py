from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import random
import generator

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = True
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337ksdfwh34132w'

#TODO Add a teller class to do teller functions through?? What should be done with buy/sell cash if not. (I.e. only effects Vault(maybe) and teller GL)

class Teller(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, cashbal, cashdenom):
        self.cashbal = 0
        self.cashdenom = [0,0,0,0,0,0,0,0,0,0,0,0,0]

"""    def balance():
        done = False
        while done == False:
            hundreds =  # pull input from UI #TODO
            fifties =
            twenties =
            tens =
            fives =
            twos = 
            ones =
            dollarc = 
            halves = 
            quarters =
            dimes = 
            nickels = 
            penies = 

    def changecash(trancode, amount):  #TODO
        cur_cash = self.cashbal
"""

class Customer():   #need to add db.Model after database implementation for each Class
    #id = db.Column(db.Integer, primary_key=True)

    def __init__(self, id, ssn, name, dob):
        self.id = id    #Will likely change after Database is added 
        self.ssn = ssn
        self.name = name
        self.dob = dob


class Account():
                            #id = db.Column(db.Integer, primary_key=True)
    def __init__(self, ssns, acctn, bal, prod, date_opened):
                                        #Join with Customer DB via SSN #TODO
        self.acctn = id
        self.prod = prod
        self. date_opened = date_opened
        self.ssns = ssns

        #Store the parameter translist to easily do a query on all transactions associated with an account
"""        #Join with Trans DB to call for specific Account number #TODO

    def print_pah():
        customername = self.sah
        print(customername)

    def deposit(): #Still needs input #TODO
        #variable allocation
        #calculate new balance of teller GL
        #Determine if you want to devide the Teller GL function into a sub function to call with the withdrawl function aswell

    def withdrawl(): #TODO

    def acctinq(): #TODO
"""


    
class Trans():
    #id = db.Column(db.Integer, primary_key=True)

    def __init__(self, id, time, amount, description, trancode): #trancode needs to be direction specific to determine debit/credit #TODO
        self.id = id        # removed and reverted to previous commented line when moved to database
        self.time = datetime                                        #self.Account = #import accountdb
        self.amount = amount
        self.description = description
        self.trancode = trancode

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

    for account in account_list:
        owner_ssn = account.pop()
        date_opened = account.pop()
        prod = account.pop()
        bal = account.pop()
        acct_number = account.pop()
        new_Account = Account(owner_ssn, acct_number, bal, prod, date_opened)
        new_Account_list.append(new_Account)

    for transaction in trans_list:
        tran_balance = transaction.pop()
        desc = transaction.pop()
        trancode = transaction.pop()
        time = transaction.pop()
        id = transaction.pop()
        new_tran = Trans(id, time, tran_balance, desc, trancode)
        new_Trans_list.append(new_tran)

    return new_Customer_list, new_Account_list, new_Trans_list


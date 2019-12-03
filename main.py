from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from datetime import time
from datetime import datetime

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
        self.cashbal = 
        self cashdenom = [0,0,0,0,0,0,0,0,0,0,0,0,0]

    def balance():
        done = False
        while done = False:
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


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, ssn, name, dob):
        self.ssn = ssn
        self.name = name
        self.dob = dob


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, pah, sah, acctn, bal, prod, date_opened, ave_balance, translist):
        #Join with Customer DB via SSN #TODO
        self.acctn = id
        self.balance = ave_balance
        self.prod = prod
        self. date_opened = date_opened
        #Join with Trans DB to call for specific Account number #TODO

    def print_pah():
        customername = self.sah
        print(customername)

    def deposit(): #Still needs input #TODO
        #variable allocation
        #calculate new balance of teller GL
        #Determine if you want to devide the Teller GL function into a sub function to call with the withdrawl function aswell

    def withdrawl(): #TODO

    def acctinq(): #TODO



    
class Trans(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, time, Account, amount, description, trancode): #trancode needs to be direction specific to determine debit/credit #TODO
        self.time = datetime
        self.Account = #import accountdb
        self.amount = amount
        self.description = description
        self.trancode = trancode

    



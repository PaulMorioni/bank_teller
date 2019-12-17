from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import random

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

    def __init__(self, ssns, acctn, bal, prod, date_opened, ave_balance, translist):
        #Join with Customer DB via SSN #TODO
        self.acctn = id
        self.balance = ave_balance
        self.prod = prod
        self. date_opened = date_opened
        self.ssns = ssns
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

    




class Generator():

    def random_n_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return random.randint(range_start,range_end)


    def gen_n_digit_unique(amount, number_of_digits):
        list_of_numbers = []
        for i in amount:
            if len(list_of_numbers) = 0:
                nnum = Generator.random_n_digits(number_of_digits)
                list_of_numbers.append(nnum)
            else:
                nnum = Generator.random_n_digits(number_of_digits)
                while nnum in list_of_numbers:
                    nnum = Generator.random_n_digits(number_of_digits)
                list_of_numbers.append(nnum)
        
        return list_of_numbers
    
    def random_amount():
        amount = round(random.uniform(1.5,500.5),2)
        return amount

    def random_datetime(start, end):
        delta = end - start
        int_delta = (timedelta.days * 24 * 60 * 60) + timedelta.seconds
        random_second = random.randrange(int_delta)
        return start + timedelta(seconds=random_second)

    

    def gen_customer(amount):
        customer_list = []
        passing_ssn = []
        active_ssn = gen_n_digit_unique(amount, 9)
        for i in amount:
            id = 0 + i
            ssn = list.pop(active_ssn)
            name = random.choice(name_list)
            dob = random_datetime()
            customer = [id, ssn, name, dob]
            customer_list.append(customer)
            passing_ssn.append(ssn)
        return customer_list, passing_ssn
            


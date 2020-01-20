#from flask import Flask, request, redirect, render_template, session, flash
#from flask_sqlalchemy import SQLAlchemy
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import random
import generator

__name__ = '__main__'


#Trancodes shouldnt be stored in a CSV trancode is too functional to be handled that way. hardcode into its own module or into main module.

'''
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

    def balance():
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
'''


class Customer():   #need to add db.Model after database implementation for each Class
    #id = db.Column(db.Integer, primary_key=True)

    def __init__(self, id, ssn, name, dob):
        self.id = id    #Will likely change after Database is added 
        self.ssn = ssn
        self.name = name
        self.dob = dob

    def str_id(self):
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
    def store(customer):
        str_id = customer.str_id()
        str_ssn = customer.str_ssn()
        name = customer.name
        str_dob = customer.str_dob()
        generator.write_cust(str_id, str_ssn, name, str_dob)

    @staticmethod
    def make_customer():

        cust_id = input('Enter ID Number: ')
        ssn = input('Enter SSN: ')
        name = input('Enter Full Name: ')
        dob = input('Enter Date of Birth:')
        new_customer = Customer(cust_id, ssn, name, dob)
        Customer.store(new_customer)
        return new_customer



class Account():
                            #id = db.Column(db.Integer, primary_key=True)
    def __init__(self, ssns, acctn, bal, prod, date_opened):
                                        #Join with Customer DB via SSN #TODO
        self.acctn = acctn
        self.prod = prod
        self. date_opened = date_opened
        self.ssns = ssns
        self.bal = bal

        #Store the parameter translist to easily do a query on all transactions associated with an account
                                        # #Join with Trans DB to call for specific Account number #TODO

    @staticmethod
    def store(account):
        dt_date_opened = account.date_opened
        ssns = account.ssns
        acctn = account.acctn
        bal = account.bal
        prod = account.prod
        date_opened = dt_date_opened.strftime('%m/%d/%Y %I:%M %p')

        generator.write_account(ssns,acctn, bal, prod, date_opened)

    @staticmethod
    def make_account():
        ssns = []
        acctn = input('Enter Account Number: ')
        number_of_owners = int(input('Enter Number of Account Owners: '))
        for i in range(0,number_of_owners):
            print(i)
            ssn = input('Enter SSN: ')
            ssns.append(ssn)
        starting_balance = input('Enter Amount of Initial Deposit: ')
        prod = input('Enter Product Name: ')
        date_opened = datetime.now()
        new_acct = Account(ssns,acctn, starting_balance, prod, date_opened)
        Account.store(new_acct)
        return new_acct

'''
    def deposit(): #Still needs input #TODO
        #variable allocation
        #calculate new balance of teller GL
        #Determine if you want to devide the Teller GL function into a sub function to call with the withdrawl function aswell

    def withdrawl(): #TODO

    def acctinq(): #TODO

'''

    
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
        new_Customer = Customer(id, ssn, name, dob) #TODO problem here
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


def main():

    Account.make_account()



if __name__ == '__main__':
    main()
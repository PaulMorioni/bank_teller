from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import datetime
import random
import generator
import re

__name__ = '__main__'




app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = True
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


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Columnd(db.String(100))
    dob = db.Column(db.Integer)
    ssn = db.Column(db.Integer)

    def __init__(self, ssn, name, dob):
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

    @staticmethod
    def import_customers():
        customer_obj_list = []
        stored_customer_list = generator.read_cust()
        for customer_atribute_list in stored_customer_list:
            cust_id = customer_atribute_list[0]
            ssn = customer_atribute_list[1]
            name = customer_atribute_list[2]
            dob = customer_atribute_list[3]
            stored_customer_object = Customer(cust_id, ssn, name, dob)
            customer_obj_list.append(stored_customer_object)
        return customer_obj_list



class Account(db.Model):
    acctn = db.Column(db.Integer, primary_key=True)
    prod = db.Column(db.String(50))
    date_opened = db.Column(db.String(25))
    ssns = db.relationship('Customer', backref='ssn')
    transactions = db.relationship('Trans', backref='account')
    #TODO Need to set foreign keys for join table with customer ssn
    def __init__(self, ssns, acctn, bal, prod, date_opened):
                                        #Join with Customer DB via SSN #TODO
        self.acctn = acctn
        self.prod = prod
        self.date_opened = date_opened
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

    @staticmethod
    def import_accounts():
        account_obj_list = []
        stored_account_list = generator.read_account()
        for account_atribute_list in stored_account_list:
            ssns = account_atribute_list[0]
            acctn = account_atribute_list[1]
            starting_balance = account_atribute_list[2]
            prod = account_atribute_list[3]
            date_opened = account_atribute_list[4]
            account_object = Account(ssns, acctn, starting_balance, prod, date_opened)
            account_obj_list.append(account_object)
        return account_obj_list




class Trans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    amount = db.Column(db.String(50))
    description = db.Column(db.String(100))
    trancode = db.Column(db.Integer)
    account = db.Column(db.Integer, db.ForeignKey('Account.acctn'))

    def __init__(self, id : int, tran_time : datetime, amount : float, description : str, trancode: int, account: str):
        self.id = id
        self.time = tran_time
        self.amount = amount
        self.description = description
        self.trancode = trancode
        self.account = account


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

    @staticmethod
    def store(tran):
        dt_date_opened = tran.time
        tran_id = tran.id
        account = tran.account
        amount = tran.amount
        desc = tran.description
        trancode = tran.trancode
        tran_time = dt_date_opened.strftime('%m/%d/%Y %I:%M %p') #Why isnt time a date, it shouldnt already be a string until this line

        generator.write_tran(tran_id, tran_time, amount, desc, trancode, account)

    @staticmethod
    def import_trans():
        tran_obj_list = []
        stored_tran_list = generator.read_tran()
        for tran_attribute_list in stored_tran_list:
            tran_id = tran_attribute_list[0]
            tran_time = tran_attribute_list[1]
            amount = tran_attribute_list[2]
            desc = tran_attribute_list[3]
            trancode = tran_attribute_list[4]
            account = tran_attribute_list[5]
            tran_object = Trans(tran_id, tran_time, amount, desc, trancode, account)
            tran_obj_list.append(tran_object)
        return tran_obj_list



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


def main():

all_customers, all_accounts, all_trans = startup()




if __name__ == '__main__':
    main()
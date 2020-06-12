from flask import Flask, request, redirect, render_template, session, flash, jsonify
from flask_assets import Bundle, Environment
from flask_sqlalchemy import SQLAlchemy
from datetime import *
import random
import re
from forms import *
import locale
from decimal import *


__name__ = '__main__'
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bank_teller:bankandtrust@localhost:8899/bank_teller'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'y337ksdfwh34132w'
locale.setlocale( locale.LC_ALL,'English_United States.1252')

assets = Environment(app)
        
#js = Bundle('jquery.min.js', 'jquery.min.map', 'popper.min.js', 'popper.min.js.map', 'bootstrap.min.js', 'bootstrap.min.js.map', 'balance.js', output='gen/main.js')

#assets.register('main_js', js)


debit_trancodes = [50, 500, 150]
credit_trancodes = [13, 113, 400]


class Teller(db.Model):

    teller_id = db.Column(db.Integer, primary_key=True)
    cashbal = db.Column(db.Numeric(18,4))
    cashdenom = db.Column(db.String(400))
    #transactions = db.relationship('Trans', backref='teller', lazy='dynamic')

    def __init__(self, teller_id):
        self.cashbal = 0
        self.cashdenom = '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'
    
    def changecash(self, trancode, amount):
        cur_cash = self.cashbal
        if trancode in credit_trancodes: #credit relative to perspective account will be opposite of teller GL (i.e. credit trancodes will debit teller)
            self.cashbal = cur_cash + amount
        elif trancode in debit_trancodes: #opposite of above comment
            self.cashbal = cur_cash - amount
        
        db.session.commit()

    def rounded_amount(self):
        rounded_amount = locale.currency(self.cashbal, grouping=True)
        return rounded_amount

    def buy(self, amount):
        cur_cash = self.cashbal
        self.cashbal = cur_cash + amount
        db.session.commit()

    def sell(self, amount):
        cur_cash = self.cashbal
        self.cashbal = cur_cash - amount
        db.session.commit()

    def parse_denom(self):
        denom_list = self.cashdenom.split(",")
        return denom_list

    def balance(self, list_of_denom):
        str_denom = []
        for denom in list_of_denom:
            str_denom.append(str(denom))    #turns list of integers into string
        
        new_denom = ','.join(str_denom) #concatenates list of string to be DB friendly
        self.cashdenom = new_denom
        db.session.commit()



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

    @staticmethod
    def search_customer(attr_search, search_param):
        if attr_search == 'name':
            search_return = Customer.query.filter(Customer.name.contains(search_param)).all()
        elif attr_search == 'ssn':
            search_return = Customer.query.filter(Customer.ssn.contains(search_param)).all()

        return search_return

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
        if trancode in credit_trancodes:
            new_balance = current_balance + amount
            self.bal = new_balance
            db.session.commit()
        
        elif trancode in debit_trancodes:
            new_balance = current_balance - amount
            self.bal = new_balance
            db.session.commit()

    def owners(self):
        
        owners = []

        results = db.session.query(accounts_owners).filter(accounts_owners.c.account_id==self.account_id).all()
        
        for result in results:
            owners.append(Customer.query.filter_by(customer_id=result.customer_id).first()) #returns customer from Table query object

        return owners

    def formatted_balance(self):
        formatted_bal = locale.currency(self.bal, grouping=True)
        return formatted_bal

    def add_owner(self, customer):
        new_owners_accounts = customer.accounts
        if self in new_owners_accounts:
            raise 'Account already has that owner'
        else:
            customer.accounts.append(self)
            db.session.commit()

    def primary_owner(self):
        owners = self.owners()
        if owners:
            primary_owner = owners[0]
            return primary_owner
        else:
            return None

    @staticmethod
    def search_account(attr_search, search_param):
        if attr_search == 'account_number':
            search_return = Account.query.filter(Account.acctn.contains(search_param)).all()

        elif attr_search == 'date_opened':
            search_return = Account.query.filter(Account.date_opened.contains(search_param)).all()

        elif attr_search == 'product':
            search_return = Account.query.filter(Account.prod.contains(search_param)).all()

        if search_return:
            return search_return


class Trans(db.Model):
    tran_id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(25))
    amount = db.Column(db.Numeric(18,4))
    description = db.Column(db.String(100))
    trancode = db.Column(db.Integer)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'))
    #teller_id = db.Column(db.Integer, db.ForeignKey('teller.teller_id'))    

    def __init__(self, tran_time, amount, description, trancode, teller_id = None):
        self.time = tran_time
        self.amount = amount
        self.description = description
        self.trancode = trancode
        self.teller_id = teller_id
        
    def rounded_amount(self):
        rounded_amount = locale.currency(self.amount, grouping=True)
        return rounded_amount

    def time_datetime(self):
            str_tran_date = self.time
            tran_datetime = datetime.strptime(str_tran_date,'%x , %X')
            return tran_datetime
    
    def formatted_amount(self):
        fmt_amt = locale.currency(self.amount, grouping=True)
        return fmt_amt

    def set_teller_id(self, teller_id):
        self.teller_id = teller_id

    def isDebit(self):  #Determines debit relative to account_id
        if self.trancode in debit_trancodes:
            return True
        else:
            return False


@app.before_request #TODO fix issue with not loading JS until after this request
def require_login():
    allowed_routes = ['teller_login', 'home']
    if request.endpoint not in allowed_routes and 'teller_id' not in session:
        return redirect('/teller_login')


@app.route('/teller_login', methods = ['POST', 'GET'])
def teller_login():
    errors = []
    teller_id = ''
    form = TellerLoginForm()
    if request.method == 'GET':

        return render_template('teller_login.html', form=form)

    if request.method == 'POST':
        teller_id = form.teller_id.data
        teller = Teller.query.filter_by(teller_id=teller_id).first()
        if teller:
            session['teller_id'] = teller_id
            flash('Logged In')
            return redirect('/home')
        else:
            error = 'Teller ID Not Found'
            errors.append(error)
            return render_template('teller_login.html', form=form, errors=errors)


@app.route('/home', methods = ['POST', 'GET'])
def home():
    
    return render_template('home.html')


@app.route('/deposit', methods = ['POST', 'GET'])
def deposit():
    errors = []
    form = DepositForm()
    trancode = 13

    if request.method == 'GET':
        
        return render_template('deposit.html', account_readout = False, form=form)

    else:
        account_number = form.account.data

        account = Account.query.filter_by(acctn=account_number).first() #retireves account

        if account: #If account could be located


            cash_amount = form.cash_amount.data
            check_amount = form.check_amount.data
            amount = cash_amount + check_amount

            teller_id = session['teller_id']
            teller = Teller.query.filter_by(teller_id=teller_id).first()

            teller.changecash(trancode, amount)

            desc = 'Deposit with Teller ' + str(teller_id)
            tran_time = datetime.now()
            str_tran_time = tran_time.strftime('%x , %X')

            new_deposit = Trans(str_tran_time, amount, desc, trancode)

            account.transactions.append(new_deposit)

            db.session.add(new_deposit)
            account.calc_balance(trancode, amount)
            db.session.commit()

            return render_template('success.html' )
    
        else:
            error = "Account Not Found"
            errors.append(error)
            return render_template('deposit.html', account_readout = False, form=form, errors=errors)

        
@app.route('/withdrawl', methods = ['POST', 'GET'])
def withdrawl():

    errors = []
    form = WithdrawlForm()
    trancode = 50

    if request.method == 'GET':
        
        return render_template('withdrawl.html', account_readout = False, form=form)

    else:
        account_number = form.account.data

        account = Account.query.filter_by(acctn=account_number).first() # finds account

        if account:

            amount = form.amount.data

            teller_id = session['teller_id']
            teller = Teller.query.filter_by(teller_id=teller_id).first()

            desc = 'Withdrawl with Teller ' + str(teller_id)
            tran_time = datetime.now()
            str_tran_time = tran_time.strftime('%x , %X')

            new_withdrawl = Trans(str_tran_time, amount, desc, trancode)    # makes new transaction

            account.transactions.append(new_withdrawl)  # adds transaction to account

            teller.changecash(trancode, amount)

            db.session.add(new_withdrawl)
            account.calc_balance(trancode, amount)  #calculates balance of account
            db.session.commit()

            return render_template('success.html' )

        else:
            errors.append('Account Not Found')
            return render_template('withdrawl.html', account_readout = False, form=form, errors=errors)


@app.route('/transfer', methods = ['POST', 'GET'])
def transfer():
    errors = []
    form = TransferForm()
    debit_trancode = 50
    credit_trancode = 13
    

    if request.method == 'GET':
        return render_template('transfer.html', form=form)

    else:   # preforms transfer upon validation
        if form.validate():
            debit_account_num = form.debit_account.data
            credit_account_num = form.credit_account.data
            amount = form.amount.data

            debit_account =  Account.query.filter_by(acctn=credit_account_num).first()   #Retrieves accounts
            credit_account = Account.query.filter_by(acctn=debit_account_num).first()

            if credit_account and debit_account:

                debit_desc = 'Transfer to ' + str(debit_account_num)      #This block organizes data to create transaction
                credit_desc = 'Transfer from ' + str(credit_account_num)
                tran_time = datetime.now()
                str_tran_time = tran_time.strftime('%x , %X')


                debit_trans = Trans(str_tran_time,amount,debit_desc, debit_trancode)    #creates transactions to be added to accounts' list
                credit_trans = Trans(str_tran_time,amount, credit_desc, credit_trancode)


                debit_account.transactions.append(debit_trans)  #Adds transactions to respective accounts
                credit_account.transactions.append(credit_trans)

                db.session.add(debit_trans)
                db.session.add(credit_trans)

                debit_account.calc_balance(debit_trans.trancode, amount)    #calculates new balance of account
                credit_account.calc_balance(credit_trans.trancode, amount)
                db.session.commit()

                return render_template('success.html')

            else:
                if debit_account:
                    error = 'Credit Account not found'
                elif credit_account:
                    error = 'Debit Account not found'
                elif not debit_account or credit_account:
                    error = 'Accounts not found'
                errors.append(error)
                return render_template('transfer.html', form=form, errors=errors)

        else:
            return render_template('transfer.html', form=form)
    
    
@app.route('/inquiry', methods = ['POST', 'GET'])
def inquiry(): 
    form = InquiryForm()
    account_id = request.args.get('acct')
    errors = []

    if request.method == 'GET' and account_id: #determines if link from search page or if navigation to form
        account = Account.query.filter_by(account_id=account_id).first()
        customers = account.owners()    

        return render_template('inquiry.html', account_readout=False, customers=customers, account=account, inquiry=True)

    elif request.method == 'GET' and not account_id:
        return render_template('inquiry.html', form=form, account_readout=False)
    
    if request.method == 'POST':

        if form.validate() == False:
            errors.append(form.error)
            return render_template('inquiry.html', form=form, account_readout=False, errors=errors)

        if form.validate():
            account_number = form.account_number.data
            account = Account.query.filter_by(acctn=account_number).first()  #Add account submited by form to accounts
            if account:
                customers = account.owners()    #Add customers of selected account to customers
                return render_template('inquiry.html', inquiry=True, customers=customers, account=account)
            else:
                error = "Account does not exist"
                errors.append(error)
                return render_template('inquiry.html', form=form, account_readout=False, errors=errors)
            
             
@app.route('/balance', methods = ['POST', 'GET'])
def balance():
    form = BalanceForm()    #a list of form objects that can be looped over to either effect data with iterated string, or fill in data of prior balance   
    
    form_elements = [form.hundreds, form.fifties, form.twenties, form.tens, form.fives, form.twos, form.ones, form.dollarc, form.halves, form.quarters, form.dimes, form.nickels, form.pennies,
    form.hundreds_bundles, form.fifties_bundles, form.twenties_bundles, form.tens_bundles, form.fives_bundles, form.twos_bundles,
    form.ones_bundles, form.dollarc_rolls, form.halves_rolls, form.quarters_rolls, form.dimes_rolls, form.nickels_rolls, form.pennies_rolls]
    
    new_denom = []

    teller_id = session['teller_id']
    teller = Teller.query.filter_by(teller_id=teller_id).first()

    if request.method == 'GET':

        if teller.cashdenom == '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0':
            return render_template('balance.html', form=form, teller=teller)

        else:
            list_of_denom = teller.parse_denom()
            for i in range(len(form_elements)): # elements and cashdenom list is the same length, so i is used as index for both
                current_element = form_elements[i]  #selects form element of index 
                current_denom = list_of_denom[i]    #selects case value of coresponding denomination
                current_element.data = Decimal(current_denom)    #sets previously entered denomination to form element value so prior balance history isn't lost

            return render_template('balance.html', form=form, teller=teller)

    if request.method == 'POST':
        for element in form_elements:   
            new_denom.append(element.data)  #retrieves value of each form element in order
        teller.balance(new_denom)

        return render_template('Success.html')
        

@app.route('/buy', methods = ['POST', 'GET'])
def buy():

    form = TellerBuyForm()

    if request.method == 'GET':

        return render_template('buy.html', form=form)

    if request.method == 'POST':
        current_teller_id  = session['teller_id']
        current_teller = Teller.query.filter_by(teller_id=current_teller_id).first()
            #buy_from_id = form.buy_from_id.data #does not effect cash bal of other teller, other teller would perform debit transaction(sell function)
            #description and buy from teller would be added after teller cash log is added to Database to track buy and sells on a GL. General Ledger functionality will be added at a later date.
        amount = form.amount.data
        current_teller.buy(amount)

        return redirect('/home')


@app.route('/sell', methods = ['POST', 'GET'])
def sell():

    form = TellerSellForm()

    if request.method == 'GET':

        return render_template('sell.html', form=form)

    if request.method == 'POST':
        current_teller_id  = session['teller_id']
        current_teller = Teller.query.filter_by(teller_id=current_teller_id).first()
            #sell_to_id = form.sell_to_id.data #does not effect cash bal of other teller, other teller would perform debit transaction(sell function)
            #description and buy from teller would be added after teller cash log is added to Database to track buy and sells on a GL. General Ledger functionality will be added at a later date.
        amount = form.amount.data
        current_teller.sell(amount)

        return redirect('/home')


@app.route('/new_account', methods = ['POST', 'GET'])   #TODO add cash and check deposit fields to allow for teller cash handeling
def make_account():
    form = NewAccountForm()
    error = []
    trancode = 13
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('new_account.html', account_readout=False, form=form)
        else:

            account_number = form.account_number.data
            primary_ssn = form.primary_ssn.data
            opening_deposit =form.bal.data
            product = request.form['product']
            date_opened = datetime.now()
            str_date_opened = date_opened.strftime("%x")
            str_tran_time = date_opened.strftime('%x , %X')

            customer = Customer.query.filter_by(ssn=primary_ssn).first()
            if customer:      
                owner_ssn = customer.ssn
                account = Account(owner_ssn, account_number, opening_deposit, product, str_date_opened)
                
                desc = 'Opening Deposit'
                opening_transaction = Trans(str_tran_time, opening_deposit, desc, trancode)
                account.transactions.append(opening_transaction)
                

                customer.accounts.append(account)       #Relates customer to account owner.

                db.session.add(account)
                db.session.commit()
                return render_template('success.html', title="Success")

            else:
                error = "Customer Does not Exist"
                errors.append(error)
                return render_template('new_account.html', errors=errors, account_readout=False, form=form)
            
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

@app.route('/search', methods = ['POST', 'GET']) 
def search():
    wform = SearchForm()

    customer_attr_types = [('name', 'Name'), ('ssn', 'SSN')]

    wform.attr_type.choices = customer_attr_types    

    if request.method == 'GET':
        
        return render_template('search.html', form=wform)


    if request.method == 'POST':   #Uses radio button to determine which Class search function to call.
        search_type = request.form['searchType']
        if search_type == 'customer':
            customers = Customer.search_customer(wform.attr_type.data, wform.search_param.data)
            return render_template( 'search.html', search_return=True, customers=customers)

        if search_type == 'account':  
            accounts = Account.search_account(wform.attr_type.data, wform.search_param.data)
            return render_template('search.html', search_return=True, accounts=accounts)
        
    else:
        return render_template('search.html', form=wform)


@app.route('/customer')
def customer_inquiry():
    customer_id = request.args.get("cid")
    customer = Customer.query.filter_by(customer_id=customer_id).first()    
    accounts = customer.accounts

    return render_template('customer.html', customer=customer, accounts=accounts)


@app.route('/add_customer', methods=['GET', 'POST']) #TODO add more functionality with JS?
def add_customer():
    form = CustomerForm()

    if request.method == 'GET':
        return render_template('add_customer.html', form=form)

    if request.method == 'POST':
        if form.validate():
            account_num = form.account.data
            customer_ssn = form.new_ssn.data

            account = Account.query.filter_by(acctn=account_num).first()
            customer = Customer.query.filter_by(ssn=customer_ssn).first()

            account.add_owner(customer)

            return render_template('success.html')
        else: 
            return render_template('add_customer.html', form=form)




if __name__ == '__main__':

    app.run()

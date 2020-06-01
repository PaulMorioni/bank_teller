from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import *
import random
import re
from forms import *
import locale



__name__ = '__main__'
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bank_teller:bankandtrust@localhost:8889/bank_teller'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337ksdfwh34132w'
locale.setlocale( locale.LC_ALL,'English_United States.1252')

debit_trancodes = [50, 500, 150]
credit_trancodes = [13, 113, 400]


#TODO Add a teller class to do teller functions through?? What should be done with buy/sell cash if not. (I.e. only effects Vault(maybe) and teller GL)

class Teller(db.Model):

    teller_id = db.Column(db.Integer, primary_key=True)
    cashbal = db.Column(db.Numeric(18,4))
    cashdenom = db.Column(db.String(20))

    def __init__(self, teller_id):
        self.cashbal = 0
        self.cashdenom = '0,0,0,0,0,0,0,0,0,0,0,0,0'
    

    def changecash(self, trancode, amount):  #TODO
        cur_cash = self.cashbal
        if trancode in credit_trancodes: #credit relative to perspective account will be opposite of teller GL (i.e. credit trancodes will debit teller)
            self.cashbal = cur_cash - amount
        elif trancode in debit_trancodes: #opposite of above comment
            self.cashbal = cur_cash + amount
        
        db.session.commit()


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
    def search_customer(attr_search, search_param): #TODO determine best way to do fuzzy search
        if attr_search == 'name':
            search_return = Customer.query.filter(Customer.name.like(search_param)).all()
        elif attr_search == 'dob':
            search_return = Customer.query.filter_by(dob=search_param).all()
        elif attr_search == 'ssn':
            search_return = Customer.query.filter_by(ssn=search_param).all()

        return search_return

class Account(db.Model):    #TODO add function to calculate running balance with transactions for inquiry screen
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

    @staticmethod
    def search_account(attr_search, search_param):
        search_return = Account.query.filter_by(attr_search=search_param).all()
        return search_return


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
    
    def formatted_amount(self):
        fmt_amt = locale.currency(self.amount, grouping=True)
        return fmt_amt


@app.before_request
def require_login():
    allowed_routes = ['teller_login', 'home']
    if request.endpoint not in allowed_routes and 'teller_id' not in session:
        return redirect('/teller_login')


@app.route('/teller_login', methods = ['POST', 'GET'])
def teller_login():
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


@app.route('/home', methods = ['POST', 'GET'])
def home():
    
    return render_template('home.html')


@app.route('/deposit', methods = ['POST', 'GET'])
def deposit():
    form = DepositForm()
    trancode = 13

    if request.method == 'GET':
        
        return render_template('deposit.html', account_readout = False, form=form)

    else:
        account_number = form.account.data

        account = Account.query.filter_by(acctn=account_number).first() #retireves account

        if account: #If account could be located

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
    
        else:
            error = "Account Not Found"
            return render_template('deposit.html', account_readout = False, form=form, error=error)

        


@app.route('/withdrawl', methods = ['POST', 'GET'])
def withdrawl():

    form = WithdrawlForm()
    trancode = 50

    if request.method == 'GET':
        
        return render_template('withdrawl.html', account_readout = False, form=form)

    else:   #TODO add catch for account that couldnt be found
        account_number = form.account.data

        account = Account.query.filter_by(acctn=account_number).first() # finds account

        amount = form.amount.data

        desc = 'Withdrawl with Teller'
        tran_time = datetime.now()
        str_tran_time = tran_time.strftime('%x , %X')

        new_withdrawl = Trans(str_tran_time, amount, desc, trancode)    # makes new transaction

        account.transactions.append(new_withdrawl)  # adds transaction to account

        db.session.add(new_withdrawl)
        account.calc_balance(trancode, amount)  #calculates balance of account
        db.session.commit()

        return render_template('success.html' )


@app.route('/transfer', methods = ['POST', 'GET'])
def transfer():
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
                return render_template('transfer.html', form=form, error=error)

        else:
            return render_template('transfer.html', form=form)
    
    


@app.route('/inquiry', methods = ['POST', 'GET'])
def inquiry():  #TODO add running balance and color coding to debit credit
    form = InquiryForm()
    account_id = request.args.get('acct')

    if request.method == 'GET' and account_id: #determines if link from search page or if navigation to form
        account = Account.query.filter_by(account_id=account_id).first()
        customers = account.owners()    

        return render_template('inquiry.html', account_readout=False, customers=customers, account=account, inquiry=True)

    elif request.method == 'GET' and not account_id:
        return render_template('inquiry.html', form=form, account_readout=False)
    
    if request.method == 'POST':

        if form.validate() == False:
            error = form.error
            return render_template('inquiry.html', form=form, account_readout=False, error=error)

        if form.validate():
            account_number = form.account_number.data
            account = Account.query.filter_by(acctn=account_number).first()  #Add account submited by form to accounts
            if account:
                customers = account.owners()    #Add customers of selected account to customers
                return render_template('inquiry.html', inquiry=True, customers=customers, account=account)
            else:
                error = "Account does not exist"
                return render_template('inquiry.html', form=form, account_readout=False, error=error)
            
            


@app.route('/balance', methods = ['POST', 'GET'])
def balance():
    form = BalanceForm()
    if request.method == 'GET':
        teller_id = session['teller_id']
        teller = Teller.query.filter_by(teller_id=teller_id).first()

        if teller.cashdenom == '0,0,0,0,0,0,0,0,0,0,0,0,0':
            return render_template('balance.html', form=form, teller=teller)

        else:
            list_of_denom = teller.parse_denom()
            #convert to touples? so that we can loop over default values of form

        


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

@app.route('/search', methods = ['POST', 'GET'])    #TODO add fuzzy search functionality.propbably with postgresql
def search():
    form = SearchForm()
    form.attr_type.choices = [('name', 'Name'), ('dob', 'Date of Birth'),('ssn', 'SSN')]
    
    if request.method == 'GET':
        
        return render_template('search.html', form=form)


    if request.method == 'POST' and form.validate():   #Uses radio button to determine which Class search function to call.
        if form.search_type.data == 'customer':
            customers = Customer.search_customer(form.attr_type.data, form.search_param.data)
            return render_template('search.html', search_return=True, customers=customers)
        if form.search_type == 'account':   #TODO fix account search functionality
            accounts = Account.search_account(form.attr_type.data, form.search_param.data)
            return render_template('search.html', search_return=True, accounts=accounts)
        
    else:
        return render_template('search.html', form=form)

@app.route('/customer')
def customer_inquiry():
    customer_id = request.args.get("cid")
    customer = Customer.query.filter_by(customer_id=customer_id).first()    
    accounts = customer.accounts

    return render_template('customer.html', customer=customer, accounts=accounts)



@app.route('/add_customer', methods=['GET', 'POST'])
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

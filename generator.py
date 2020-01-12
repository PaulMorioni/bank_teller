from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import random
import main

def random_n_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return random.randint(range_start,range_end)


def gen_n_digit_unique(amount, number_of_digits):
    list_of_numbers = []
    for i in amount:
        if len(list_of_numbers) == 0:
            nnum = random_n_digits(number_of_digits)
            list_of_numbers.append(nnum)
        else:
            nnum = random_n_digits(number_of_digits)
            while nnum in list_of_numbers:
                nnum = random_n_digits(number_of_digits)
            list_of_numbers.append(nnum)
    
    return list_of_numbers

def random_amount():
    amount = round(random.uniform(1.5,500.5),2)
    return amount


def gen_customer(amount, months):
    customer_list = []
    passing_ssn = []
    active_ssn = gen_n_digit_unique(amount, 9)
    for i in amount:
        id = 0 + i
        ssn = list.pop(active_ssn)
        name = random.choice(name_list) #TODO Name List
        dob = random_date(months)
        customer = [id, ssn, name, dob]
        customer_list.append(customer)
        passing_ssn.append(ssn)
    return customer_list, passing_ssn
        
def gen_account(amount, ssns, months):
    active_account_numbers = gen_n_digit_unique(amount, 6)
    account_list = []
    for i in amount:
        acct = list.pop(active_account_numbers)
        bal = random_amount()
        prod = random.choice(prod_list) #TODO Product List
        date_opened = random_date(months)
        number_owner = random.randint(1,4)
        owner_ssn = []
        for i in number_owner:
            new_ssn = ssns.pop()
            owner_ssn.append(new_ssn)
            
        account = [acct, bal, prod, date_opened, owner_ssn]
        account_list.append(account)
    
    return account_list
    
def gen_transaction(amount, account_list, months):
    trans_list = []
    id_list = gen_n_digit_unique(amount, 16)
    for i in len(account_list):
        id = id_list.pop()
        time = random_date(months)
        trancode = random.choice(trancode_list) # TODO make trancode list
        desc = random.choice(desc_list) #TODO make desc list
        tran_balance = random_amount()
        tran = [time, id, tran_balance, desc, trancode]
        trans_list.append(tran)
    return trans_list
        
                
import random
import time

def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(months):
    prop = random.random()
    end = datetime.now
    start = end - months  #Unsure of ability to subract integer from datetime object
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)


def generate(cust_amount, acct_amount, trans_amount, months):
    
    customer_list, ssns = gen_customer(cust_amount, months)
    account_list = gen_account(acct_amount, ssns, months)
    trans_list = gen_transaction(trans_amount, account_list, months)

    return customer_list, account_list, trans_list
    

      
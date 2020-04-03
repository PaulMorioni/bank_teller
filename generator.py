import datetime
import pandas as pd
import numpy
import os
import random
import time as tm
import csv


def random_n_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return random.randint(range_start,range_end)


def gen_n_digit_unique(amount, number_of_digits):
    list_of_numbers = []
    amount = int(amount)
    for i in range(0, amount+1):
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
    int_amount = int(amount)
    customer_list = []
    passing_ssn = []
    active_ssn = gen_n_digit_unique(amount, 9)
    name_list = read_names()
    for i in range(0, int_amount+1):
        id = 0 + i
        ssn = active_ssn.pop(0)
        name = name_list.pop(0)
        dob = random_datetime(months)
        customer = [id, ssn, name, dob]
        customer_list.append(customer)
        passing_ssn.append(ssn)
    return customer_list, passing_ssn


def gen_account(amount, ssns, months):
    active_account_numbers = gen_n_digit_unique(amount, 6)
    account_list = []
    prod_list = read_products()
    amount = int(amount)
    for i in range(0, amount+1):
        acct = list.pop(active_account_numbers)
        bal = random_amount()
        prod = random.choice(prod_list)
        date_opened = random_datetime(months)
        number_owner = random.randint(1,4)
        owner_ssn = []
        for i in range(0, number_owner):
            new_ssn = ssns.pop(0)
            if new_ssn in owner_ssn:
                newer_ssn = ssns.pop(0)
                owner_ssn.append(newer_ssn)
                ssns.append(new_ssn)
                ssns.append(newer_ssn)

            else:
                owner_ssn.append(new_ssn)
                ssns.append(new_ssn)
            
        account = [acct, bal, prod, date_opened, owner_ssn]
        account_list.append(account)
    
    return account_list


def gen_transaction(amount, account_list, months):
    trans_list = []
    id_list = gen_n_digit_unique(amount, 16)
    desc_list = read_description()
    trancode_list = [1, 2, 3, 4, 5, 6]
    for account in account_list:
        tran_id = id_list.pop(0)
        accountn = account[0]
        tran_time = random_datetime(months)
        trancode = random.choice(trancode_list)
        desc = random.choice(desc_list)
        tran_balance = random_amount()
        tran = [tran_id, tran_time, tran_balance, desc, trancode, accountn]
        trans_list.append(tran)


    return trans_list
            

def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    str_start = start.strftime(format)
    str_end = end.strftime(format)

    stime = tm.mktime(tm.strptime(str_start, format))
    etime = tm.mktime(tm.strptime(str_end, format))
    
    ptime = stime + prop * (etime - stime)
    datetime_ptime = datetime.datetime.fromtimestamp(ptime)
    return datetime_ptime      


def month_delta(date, delta):
    delta = int(delta)
    m, y = (date.month-delta) % 12, date.year + ((date.month)-delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)


def random_datetime(amt_months):
    prop = random.random()
    end = datetime.date.today()
    start = month_delta(end, amt_months)
    zerotime = datetime.datetime.min.time()
    start_dt = datetime.datetime.combine(start, zerotime)
    end_dt = datetime.datetime.combine(end, zerotime)
    datetime_format = '%m/%d/%Y %I:%M %p'
    new_random_datetime = str_time_prop(start_dt, end_dt, datetime_format, prop)
    return new_random_datetime


def generate(cust_amount, acct_amount, trans_amount, months):
    
    customer_list, ssns = gen_customer(cust_amount, months)
    account_list = gen_account(acct_amount, ssns, months)
    trans_list = gen_transaction(trans_amount, account_list, months)

    return customer_list, account_list, trans_list
    

# Need to homogenize reading and writing csvs, either panda or csv but needs to be same module


# May soon be big enough to move to its own csv_intepret module
def read_names():
    names_series = pd.read_csv("C:\\Users\\llama\\bank_teller\\recources\\names.csv", squeeze=True)
    names_list = names_series.tolist()
    return names_list


def read_products():
    prod_series = pd.read_csv("C:\\Users\\llama\\bank_teller\\recources\\products.csv", squeeze=True)
    prod_list = prod_series.tolist()
    return prod_list


def read_description():
    desc_series = pd.read_csv("C:\\Users\\llama\\bank_teller\\recources\\trans_descriptions.csv", squeeze=True)
    desc_list = desc_series.tolist()
    return desc_list


def write_cust(cust_id, ssn, name, dob):
    with open('recources/customers.csv', mode='a') as customer_file:
        customer_writer = csv.writer(customer_file, delimiter = ',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)

        customer_writer.writerow([cust_id,ssn, name, dob])


def read_cust():
    customer_series = pd.read_csv("recources/customers.csv")
    customer_list = customer_series.values.tolist()
    return customer_list


def write_account(ssns, acctn, bal, prod, date_opened):
    with open('recources/accounts.csv', mode='a') as account_file:
        account_writer = csv.writer(account_file, delimiter = ',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)

        account_writer.writerow([ssns, acctn, bal, prod, date_opened])


def read_account():
    account_series = pd.read_csv("recources/accounts.csv")
    account_list = account_series.values.tolist()
    return account_list


def write_tran(tran_id, tran_time, tran_balance, desc, trancode, accountn):
    with open('recources/transactions.csv', mode='a') as trans_file:
        trans_writer = csv.writer(trans_file, delimiter = ',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)

        trans_writer.writerow([tran_id, tran_time, tran_balance, desc, trancode, accountn])


def read_tran():

    tran_series = pd.read_csv("recources/transactions.csv")
    tran_list = tran_series.values.tolist()
    return tran_list


'''
def selective_overwrite():
    Needs to be a function that can match a csv row with an objects ID and overwrite it with its new attribute
    preferbly modular so it doesnt have to read all 3 individually
    hope to expand to change the read and write functions to be similar

'''
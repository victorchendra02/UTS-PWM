from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete, update, Boolean, select
from sqlalchemy import text

"""
----- CREATE TABLE IN DATABASE IN TERMINAL-----
flask shell
from app import db
db.create_all()
"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/debt_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


users_table = [
    ("ladygaga", "1234", "admin"),
    ("chilling", "1234", "finance"),
    ("fiblters", "1234", "manager")
    ]


class Transactions(db.Model):
    __tablename__ = 'transactions_table'
    
    id_trns = db.Column('id_trns', db.Integer, primary_key=True)
    id_customer = db.Column(db.Integer, db.ForeignKey('customer_table.id_customer'))
    date = db.Column(db.Date)
    debt_amount = db.Column(db.Integer)
    remark = db.Column(db.Text)
    is_paid = db.Column(db.Boolean, default=False)
    
    def __init__(self, id_customer, date, debt_amount, remark):
        self.id_customer = id_customer
        self.date = date
        self.debt_amount = debt_amount
        self.remark = remark
        self.is_paid = False


class Customer(db.Model):
    __tablename__ = 'customer_table'
    
    id_customer = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(255))
    address = db.Column(db.Text)
    phone_number = db.Column(db.String(16))
    debt_total = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)

    # Create relationship
    transactions = db.relationship('Transactions', backref='transactions_table')

    def __init__(self, customer_name, address, phone_number):
        self.customer_name = customer_name
        self.address = address
        self.phone_number = phone_number
        self.debt_total = 0
        self.is_active = True
        
    def __str__(self):
        return f"Customer  :  {self.customer_name}\n" \
               f"Debt      :  {self.debt_total}\n" \
               f"Active    :  {self.is_active}"


def select_all_customer_table():
    cus_db = Customer.query.all()
    all_cus = []
    for cus in cus_db:
        all_cus.append((cus.id_customer, cus.customer_name, cus.address, cus.phone_number, cus.debt_total, cus.is_active))

    return all_cus

def select_all_transaction_table():
    trans_db = Transactions.query.all()
    all_trans = []
    for trans in trans_db:
        all_trans.append((trans.id_trns, trans.id_customer, trans.date, trans.debt_amount, trans.remark, trans.is_paid))

    return all_trans

def select_customer_name_from_customer_table():
    all_cus = Customer.query.order_by(Customer.customer_name).all()
    names = []
    for customer in all_cus:
        names.append(customer.customer_name)

    return names

def select_id_trns_from_transaction_table():
    all_id_trans = Transactions.query.order_by(Transactions.id_trns).all()
    ids = []
    for id in all_id_trans:
        ids.append(id.id_trns)

    return ids

def select_id_from_customer_table():
    all_id_cus = Customer.query.order_by(Customer.id_customer).all()
    ids = []
    for id in all_id_cus:
        ids.append(id.id_customer)

    return ids

def insert_into_customer_table(new_name, address, phone_number):
    new_cus = Customer(new_name, address, phone_number)
    db.session.add(new_cus)
    db.session.commit()

    return 

def update_transaction_table_is_paid_where_id(trans_id):
    sql = update(Transactions).where(Transactions.id_trns == trans_id).values(is_paid= 1)
    db.session.execute(sql)
    db.session.commit()

    return

def take_transactions_row_by_id(id_trans):
    sql = text(f"SELECT id_customer, debt_amount, is_paid FROM transactions_table WHERE id_trns = {id_trans}")
    result = db.engine.execute(sql)
    return result # (1, 300000, 1)


def update_customer_after_they_pay(id_cus, debt_amount):    
    sql = text(f"UPDATE customer_table SET debt_total = debt_total - {debt_amount} WHERE id_customer = {id_cus}")
    result = db.engine.execute(sql)
    return


def update_customer_after_void(id_cus, debt_amount):    
    sql = text(f"UPDATE customer_table SET debt_total = debt_total + {debt_amount} WHERE id_customer = {id_cus}")
    result = db.engine.execute(sql)
    return


def edit_profile(id_, new_name, new_address, new_ph_number):
    sql = text(f"UPDATE customer_table SET customer_name = '{new_name}' WHERE id_customer = {id_}")
    result = db.engine.execute(sql)
    return
    
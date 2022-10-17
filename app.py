from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

"""
----- CREATE TABLE IN DATABASE -----
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
# class Users(db.Model):
#     __tablename__ = 'users_table'
#    
#     username = db.Column('username', db.String(30))
#     password = db.Column('password', db.String(255))
#     roles = db.Column('roles', db.String(20)) # 3 possible roles: ["admin", "finance", "manager"]


class Transactions(db.Model):
    __tablename__ = 'transactions_table'
    
    id_trns = db.Column('id_trns', db.Integer, primary_key=True)
    # Declare foreign keys
    customer_name = db.Column(db.String(255), db.ForeignKey('customer_table.customer_name'))
    debt_amount = db.Column(db.Integer)
    
    def __init__(self, customer_name, debt_amount):
        self.customer_name = customer_name
        self.debt_amount = debt_amount


class Customer(db.Model):
    __tablename__ = 'customer_table'
    
    id_customer = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(255))
    debt_total = db.Column(db.Integer)

    # Create relation
    transactions = db.relationship('Transactions', backref='transactions_table')

    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.debt_total = 0
        
    def __str__(self):
        return f"Customer: {self.customer_name}\
                 Debt:     Rp {self.debt_total}"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_cus', methods=['GET', 'POST'])
def addcus():
    customer_name = request.form.get('cusname')
    
    new_cus = Customer(customer_name)
    print(new_cus)

    db.session.add(new_cus)
    db.session.commit()
    
    return render_template('manager.html')

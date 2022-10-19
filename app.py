from ast import Delete
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete

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

    # Create relationship
    transactions = db.relationship('Transactions', backref='transactions_table')

    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.debt_total = 0
        
    def __str__(self):
        return f"Customer:  {self.customer_name}\n" \
               f"Debt    :  {self.debt_total}"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/finance')
def finance():
    return render_template('finance.html')

@app.route('/manager')
def manager():
    return render_template('manager.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = str(request.form.get('username'))
    password = str(request.form.get('password'))

    if len(username) == 0:
        return render_template('index.html', void_username="Provide a username!")

    if len(password) == 0:
        return render_template('index.html', void_password="Provide a password!")
    else:
        username_found = False
        password_found = False
        for my_user in users_table:
            if username == my_user[0]:
                username_found = True
                if password == my_user[1]:
                    password_found = True
                    print("BERHASIL")
                    # return ke page yang sesuai role **************
                    return render_template(f'{my_user[2]}.html', correct="Correct!")
        
        if username_found == False:
            print("SALAH USERNAME")
            return render_template('index.html', wrong_username="Wrong username!")

        if password_found == False:
            print("SALAH PASSWORD")
            return render_template('index.html', wrong_username="Wrong password!")

            #     else:
            #         print("SALAH PASSWORD")
            #         return render_template('index.html', wrong_password="Wrong password!")
            # else:
            #     print("SALAH USERNAME")
            #     return render_template('index.html', wrong_username="Wrong username!")


@app.route('/add_cus', methods=['GET', 'POST'])
def addcus():
    customer_name = request.form.get('cusname')
    print(type(str(customer_name)))
    
    new_cus = Customer(customer_name)
    print(new_cus)

    db.session.add(new_cus)
    db.session.commit()
    
    return render_template('manager.html')

@app.route('/add_trans', methods=['GET', 'POST'])
def addtrans():
    customer_name = request.form.get('cusname')
    debt_amount = request.form.get('amount')

    all_cus = Customer.query.order_by(Customer.customer_name).all()
    names = []
    for customer in all_cus:
        names.append(customer.customer_name)

    if customer_name in names:
        new_trans = Transactions(customer_name, debt_amount)        

        db.session.add(new_trans)
        db.session.commit()

        return render_template('admin.html', message="Transaction added succesfully")
    else:
        return render_template('admin.html', message=f"No customer with name {customer_name}")

@app.route('/del_debt', methods=['GET', 'POST'])
def deldebt():
    # get input
    customer_name = request.form.get('cusname')

    # check if customer exist
    all_cus = Customer.query.order_by(Customer.customer_name).all()
    all_cus_names = [cus.customer_name for cus in all_cus]

    if customer_name in all_cus_names:  # if customer exist, continue; else, stop
        # check if customer have any transactions
        all_transactions = Transactions.query.order_by(Transactions.customer_name).all()
        all_cus_trans = [transaction.customer_name for transaction in all_transactions]

        if customer_name in all_cus_trans:   # if transaction exist, delete all transactions; else, stop
            sql = delete(Transactions).where(Transactions.customer_name == customer_name) 
            db.session.execute(sql)
            db.session.commit()
            return render_template('finance.html', message="Payment is succesfull")
        else:
            return render_template('finance.html', message=f"{customer_name} have no debt")
    else:
        return render_template('finance.html', message=f"No customer with name {customer_name}")

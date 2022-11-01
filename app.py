from db import *
     

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
    all_cus = select_all_customer_table()
    all_trans = select_all_transaction_table()

    return render_template('manager.html', all_customer=all_cus, all_transaction=all_trans)


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
                    return redirect(f'/{my_user[2]}')
        
        if username_found == False:
            print("SALAH USERNAME")
            return render_template('index.html', wrong_username="Wrong username!")

        if password_found == False:
            print("SALAH PASSWORD")
            return render_template('index.html', wrong_username="Wrong password!")


# Admin
@app.route('/add_trans', methods=['GET', 'POST'])
def addtrans():
    customer_id = int(request.form.get('cus_id'))
    date = request.form.get('date')
    debt_amount = request.form.get('amount')
    remark = request.form.get('remark')

    all_cus = select_all_customer_table()
    temp = []
    for cus in all_cus:
        _id = cus[0]
        status = cus[-1]
        temp.append((_id, status))
    
    print(temp)
    
        
    if (customer_id, True) in temp:

        # make new transactions
        new_trans = Transactions(customer_id, date, debt_amount, remark)  

        # update customers debt_total in debt amount 
        sql = update(Customer).where(Customer.id_customer == customer_id).values(debt_total= Customer.debt_total + debt_amount)

        db.session.add(new_trans)
        db.session.execute(sql)
        db.session.commit()

        return render_template('admin.html', message="Transaction added succesfully")
    else:
        return render_template('admin.html', message=f"No customer with id {customer_id} or Customer is disabled")



# Finance
@app.route('/pay_debt', methods=['GET', 'POST'])
def paydebt():
    # get input
    trans_id = int(request.form.get('trans_id'))
    ids = select_id_trns_from_transaction_table()

    if trans_id in ids:
        ans = take_transactions_row_by_id(trans_id)

        for x in ans:
            id_cus = x[0]
            debt_amount = x[1]
            is_paid = x[2]
            print(x[0], x[1], is_paid)
        
        if is_paid == True:
            print("already paid")
            return redirect('/finance')
        else:
            updt = update(Transactions).where(Transactions.id_trns == trans_id).values(is_paid= 1)
            db.session.execute(updt)
            db.session.commit()
            update_customer_after_they_pay(id_cus, debt_amount)
            print("paid succesfully")

            all_cus = select_all_customer_table()
            all_trans = select_all_transaction_table()
            return redirect('/finance')
    else: 
        return redirect('/finance')


# Manager
@app.route('/add_new_cus', methods=['GET', 'POST'])
def addcus():
    new_name = request.form.get('new_name')
    address = request.form.get('address')
    phone_number = request.form.get('phone_number')

    names = select_customer_name_from_customer_table()
    all_cus = select_all_customer_table()
    all_trans = select_all_transaction_table()

    if new_name in names:
        return redirect('/manager')
    else:
        insert_into_customer_table(new_name, address, phone_number)
        return redirect('/manager')


@app.route('/del_cus', methods=['GET', 'POST'])
def delcus():
    # get input
    customer_id = int(request.form.get('cus_id'))

    # check if customer exist
    all_cus = select_all_customer_table()
    all_cus_id = [cus[0] for cus in all_cus]

    if customer_id in all_cus_id:  # if customer exist, continue; else, stop
        sql = delete(Transactions).where(Transactions.id_customer == customer_id) 
        sql2 = delete(Customer).where(Customer.id_customer == customer_id) 
        db.session.execute(sql)
        db.session.execute(sql2)
        db.session.commit()
        return redirect('/manager')
    else:
        return redirect('/manager')


@app.route('/disable_cus', methods=['GET', 'POST'])
def disablecus():
    # get input
    customer_id = int(request.form.get('id'))

    # check if customer exist
    all_cus = Customer.query.all()
    all_cus_id_status = [(cus.id_customer, cus.is_active) for cus in all_cus]
    print(customer_id)

    if (customer_id, True) in all_cus_id_status:  # if customer exist, continue; else, stop
        sql = update(Customer).where(Customer.id_customer == customer_id).values(is_active= False)
        db.session.execute(sql)
        db.session.commit()
        return redirect('/manager')
    else:
        return redirect('/manager')


@app.route('/enable_cus', methods=['GET', 'POST'])
def enablecus():
    # get input
    customer_id = int(request.form.get('id'))

    # check if customer exist
    all_cus = Customer.query.all()
    all_cus_id_status = [(cus.id_customer, cus.is_active) for cus in all_cus]
    print(customer_id)

    if (customer_id, False) in all_cus_id_status:  # if customer exist, continue; else, stop
        sql = update(Customer).where(Customer.id_customer == customer_id).values(is_active= True)
        db.session.execute(sql)
        db.session.commit()
        return redirect('/manager')
    else:
        return redirect('/manager')


@app.route('/void_func', methods=['GET', 'POST'])
def void_function():
    # get input
    trans_id = int(request.form.get('trans_id'))
    ids = select_id_trns_from_transaction_table()

    if trans_id in ids:
        ans = take_transactions_row_by_id(trans_id)

        for x in ans:
            id_cus = x[0]
            debt_amount = x[1]
            is_paid = x[2]
            print(x[0], x[1], is_paid)
        
        if is_paid == False:
            print("already void")
            return redirect('/manager')
        else:
            updt = update(Transactions).where(Transactions.id_trns == trans_id).values(is_paid= 0)
            db.session.execute(updt)
            db.session.commit()
            update_customer_after_void(id_cus, debt_amount)
            print("void succesfully")
            return redirect('/manager')
    else: 
        return redirect('/manager')


@app.route('/edit', methods=['GET', 'POST'])
def edit_form():
    id_ = str(request.form.get('id_'))
    name_ = str(request.form.get('name_'))
    address = str(request.form.get('address'))
    ph_number = str(request.form.get('ph_number'))
    debt_total = str(request.form.get('debt_total'))
    is_active = str(request.form.get('is_active'))

    print(id_, name_, address, ph_number, debt_total, is_active)
    
    return render_template("/edit.html", id_=id_, name_=name_, address=address, ph_number=ph_number)



@app.route('/edit_update', methods=['GET', 'POST'])
def edit_customer():
    id_ = request.form.get('id_')
    new_name_ = str(request.form.get('new_name'))
    new_address = str(request.form.get('new_address'))
    new_ph_number = str(request.form.get('new_ph_number'))
    print(id_, new_name_, new_address, new_ph_number)

    edit_profile(id_, new_name_, new_address, new_ph_number)
    
    return redirect('/manager')


# if __name__ == '__main__':
#     app.run(host='10.252.246.205', port=5000, debug=True)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Dish(db.Model):
    __tablename__ = 'dish'

    id = db.Column(db.Integer, primary_key=True)
    d_name = db.Column(db.String())
    d_desc = db.Column(db.String())
    d_cost = db.Column(db.Float(precision=2))
    category = db.Column(db.String())
    spicy_level = db.Column(db.Integer)
    time_to_cook = db.Column(db.Integer)
    order_dishes=db.relationship('order_dish', backref='dishes', lazy='dynamic')

    def __init__(self, d_name, d_desc, d_cost, category, spicy_level, time_to_cook):
        self.d_name = d_name
        self.d_desc = d_desc
        self.d_cost = d_cost
        self.category = category
        self.spicy_level = spicy_level
        self.time_to_cook = time_to_cook

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    c_first = db.Column(db.String())
    c_last = db.Column(db.String())
    c_address = db.Column(db.String())
    c_phone = db.Column(db.Integer)
    c_city = db.Column(db.String())
    c_state = db.Column(db.String())
    c_zip = db.Column(db.Integer)
    payments = db.relationship('Payment', backref='cust', lazy='dynamic')
    
    def __init__(self, c_first, c_last, c_address, c_phone, c_city, c_state, c_zip):
        self.c_first = c_first
        self.c_last = c_last
        self.c_address = c_address
        self.c_phone = c_phone
        self.c_city = c_city
        self.c_state = c_state
        self.c_zip = c_zip

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Seating(db.Model):
    __tablename__ = 'seating'

    id = db.Column(db.Integer, primary_key=True)
    table_no = db.Column(db.Integer)
    seat_no = db.Column(db.Integer)
    seats=db.relationship('Orders', backref='seat', lazy='dynamic')
    
    def __init__(self, table_no, seat_no):
        self.table_no = table_no
        self.seat_no = seat_no
        
    def __repr__(self):
        return '<id {}>'.format(self.id)

class Promotion(db.Model):
    __tablename__ = 'promotion'

    id = db.Column(db.Integer, primary_key=True)
    discount = db.Column(db.Float(precision=2))
    p_desc = db.Column(db.String())
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    bills=db.relationship('Bill', backref='prom', lazy='dynamic')
    
    def __init__(self, discount, p_desc, start_date, end_date):
        self.discount = discount
        self.p_desc = p_desc
        self.start_date = start_date
        self.end_date = end_date
        
    def __repr__(self):
        return '<id {}>'.format(self.id)

class Emp_Job(db.Model):
    __tablename__ = 'emp_job'

    id = db.Column(db.Integer, primary_key=True)
    job_desc = db.Column(db.String())
    dept = db.Column(db.String())
    salary = db.Column(db.Integer)
    employees=db.relationship('Employee', backref='job', lazy='dynamic')
       
    def __init__(self, job_desc, dept, salary):
        self.job_desc = job_desc
        self.dept = dept
        self.salary = salary
                      
                         
    def __repr__(self):
        return '<id {}>'.format(self.id)

class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    e_first = db.Column(db.String())
    e_last = db.Column(db.String())
    e_address = db.Column(db.String())
    e_phone = db.Column(db.Integer)
    e_email = db.Column(db.String())
    e_city = db.Column(db.String())
    e_state = db.Column(db.String())
    e_zip = db.Column(db.Integer)
    job_id=db.Column(db.Integer, db.ForeignKey('emp_job.id'))
    seats=db.relationship('Orders', backref='employee', lazy='dynamic')                                           

    def __init__(self, e_first, e_last, e_address, e_phone, e_email, e_city, e_state, e_zip, job_id):
        self.e_first = e_first
        self.e_last = e_last
        self.e_address = e_address
        self.e_phone = e_phone
        self.e_email = e_email
        self.e_city = e_city
        self.e_state = e_state
        self.e_zip = e_zip
        self.job_id = job_id
                                               
    def __repr__(self):
        return '<id {}>'.format(self.id)
     
class Payment(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    medthod = db.Column(db.String())
    paid_amt = db.Column(db.Float(precision=2))
    tax = db.Column(db.Float(precision=2))
    ttl_bill = db.Column(db.Float(precision=2))
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    bills = db.relationship('Bill', backref ='pay', lazy ='dynamic')
                                                
    def __init__(self, medthod, paid_amt, tax, ttl_bill, cust_id):
        self.medthod = medthod
        self.paid_amt = paid_amt
        self.tax = tax
        self.ttl_bill = ttl_bill
        self.cust_id = cust_id
                                                    
    def __repr__(self):
        return '<id {}>'.format(self.id)


class Bill(db.Model):
    __tablename__ = 'bill'

    id = db.Column(db.Integer, primary_key=True)
    ttl_cost = db.Column(db.Float(precision=2))
    prom_id = db.Column(db.Integer, db.ForeignKey('promotion.id'))
    pay_id = db.Column(db.Integer, db.ForeignKey('payment.id'))
    seats = db.relationship('Orders', backref='bill', lazy='dynamic')
                                               
    def __init__(self, ttl_cost, prom_id, pay_id):
        self.ttl_cost = ttl_cost
        self.prom_id = prom_id
        self.pay_id = pay_id
                                                            
    def __repr__(self):
        return '<id {}>'.format(self.id)  
                                               
class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    o_date = db.Column(db.DATE)
    o_status = db.Column(db.String())
    note = db.Column(db.String())                                             
    seat_id=db.Column(db.Integer, db.ForeignKey('seating.id'))                                           
    employee_id=db.Column(db.Integer, db.ForeignKey('employee.id'))
    bill_id=db.Column(db.Integer, db.ForeignKey('bill.id'))
    order_dishes=db.relationship('order_dish', backref='order', lazy='dynamic')
                                                
    def __init__(self, o_date, o_status, note):
        self.o_date = o_date
        self.o_status = o_status
        self.note = note 
        self.seat_id = seat_id 
        self. employee_id = employee_id 
        self.bill_id = bill_id
                                                
    def __repr__(self):
        return '<id {}>'.format(self.id)   

class Order_Dish(db.Model):
    __tablename__ = 'order_dish'

    id = db.Column(db.Integer, primary_key=True)
    od_qty = db.Column(db.Integer)                                             
    order_id=db.Column(db.Integer, db.ForeignKey('orders.id'))                                           
    dishes_id=db.Column(db.Integer, db.ForeignKey('dish.id'))
                                                   
    def __init__(self, od_qty, order_id,  dishes_id):
        self.od_qty = od_qty
        self.order_id = order_id
        self. dishes_id = dishes_id       
                                                
    def __repr__(self):
        return '<id {}>'.format(self.id)
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

db = SQLAlchemy()

class Dish(db.Model):
    __tablename__ = 'dish'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    desc = db.Column(db.String())
    cost = db.Column(db.Float(precision=2))
    category = db.Column(db.String())
    spicy_level = db.Column(db.Integer)
    time_to_cook = db.Column(db.Integer)
    order_dishes=db.relationship('Order_Dish', backref='dishes', lazy='dynamic')

    def __init__(self, name, desc, cost, category, spicy_level, time_to_cook):
        self.name = d_name
        self.desc = d_desc
        self.cost = d_cost
        self.category = category
        self.spicy_level = spicy_level
        self.time_to_cook = time_to_cook

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String())
    last = db.Column(db.String())
    address = db.Column(db.String())
    phone = db.Column(db.Integer)
    city = db.Column(db.String())
    state = db.Column(db.String())
    zipcode = db.Column(db.Integer)
    payments = db.relationship('Payment', backref='cust', lazy='dynamic')
    
    def __init__(self, first, last, address, phone, city, state, zipcode):
        self.first = first
        self.last = last
        self.address = address
        self.phone = phone
        self.city = city
        self.state = state
        self.zipcode = zipcode

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
    desc = db.Column(db.String())
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    bills=db.relationship('Bill', backref='prom', lazy='dynamic')
    
    def __init__(self, discount, desc, start_date, end_date):
        self.discount = discount
        self.desc = desc
        self.start_date = start_date
        self.end_date = end_date
        
    def __repr__(self):
        return '<id {}>'.format(self.id)

class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String())
    last = db.Column(db.String())
    address = db.Column(db.String())
    phone = db.Column(db.String())
    email = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    zipcode = db.Column(db.String(5))
    seats=db.relationship('Orders', backref='employee', lazy='dynamic')                                           

    def __init__(self, first, last, address, phone, email, city, state, zipcode):
        self.first = first
        self.last = last
        self.address = address
        self.phone = phone
        self.email = email
        self.city = city
        self.state = state
        self.zipcode = zipcode
                                               
    def __repr__(self):
        return '<id {}>'.format(self.id)

    def toJSON(self):
        return jsonify({'id':self.id, \
            'first': self.first, \
            'last': self.last, \
            'address': self.address, \
            'phone': self.phone, \
            'email': self.email, \
            'city': self.city, \
            'state': self.state, \
            'zipcode': self.zipcode })
     
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
    date = db.Column(db.DATE)
    status = db.Column(db.String())
    note = db.Column(db.String())                                             
    seat_id=db.Column(db.Integer, db.ForeignKey('seating.id'))                                           
    employee_id=db.Column(db.Integer, db.ForeignKey('employee.id'))
    bill_id=db.Column(db.Integer, db.ForeignKey('bill.id'))
    order_dishes=db.relationship('Order_Dish', backref='order', lazy='dynamic')
                                                
    def __init__(self, date, status, note):
        self.date = date
        self.status = status
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
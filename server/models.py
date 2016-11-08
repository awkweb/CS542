from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from datetime import datetime

db = SQLAlchemy()

class MasterOrder(db.Model):
    __tablename__ = 'master_order'

    id = db.Column(db.Integer, primary_key=True)
    orders = db.relationship('Order', backref='bill', lazy='dynamic')
                                                            
    def __repr__(self):
        return '<id {}>'.format(self.id)  
                                          
class Dish(db.Model):
    __tablename__ = 'dish'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    cost = db.Column(db.Float(precision=2))
    category = db.Column(db.String())
    spicy_level = db.Column(db.Integer)
    order_dishes=db.relationship('Order_Dish', backref='dishes', lazy='dynamic')

    def __init__(self, name, description, cost, category, spicy_level):
        self.name = name
        self.description = description
        self.cost = cost
        self.category = category
        self.spicy_level = spicy_level

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Bill(db.Model):
    __tablename__ = 'bill'

    id = db.Column(db.Integer, primary_key=True)
    orders = db.relationship('Order', backref='bill', lazy='dynamic')
                                                                                                    
    def __repr__(self):
        return '<id {}>'.format(self.id)  
                                               
class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DATE)
    status = db.Column(db.String())
    note = db.Column(db.String())                                             
    master_order_id=db.Column(db.Integer, db.ForeignKey('master_order.id'))
    bill_id=db.Column(db.Integer, db.ForeignKey('bill.id'))
    order_dishes=db.relationship('Order_Dish', backref='order', lazy='dynamic')
                                                
    def __init__(self, note, bill_id):
        self.date = datetime.today().date()
        self.status = 'Pending'
        self.note = note
        self.bill_id = bill_id
                                                
    def __repr__(self):
        return '<id {}>'.format(self.id)   

class Order_Dish(db.Model):
    __tablename__ = 'order_dish'

    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer)                                             
    order_id=db.Column(db.Integer, db.ForeignKey('order.id'))                                           
    dish_id=db.Column(db.Integer, db.ForeignKey('dish.id'))
                                                   
    def __init__(self, qty, order_id,  dish_id):
        self.qty = qty
        self.order_id = order_id
        self. dish_id = dish_id       
                                                
    def __repr__(self):
        return '<id {}>'.format(self.id)

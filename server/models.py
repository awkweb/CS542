from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from datetime import datetime

db = SQLAlchemy()

class MasterOrder(db.Model):
    __tablename__ = 'master_order'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DATE)
    status = db.Column(db.String())
    orders = db.relationship('Order', backref='master_order', lazy='select')

    def __init__(self):
        self.date = datetime.today().date()
        self.status = 'Open'
                                                            
    def __repr__(self):
        return '<id {}>'.format(self.id)  
                                          
class Dish(db.Model):
    __tablename__ = 'dish'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.Float(precision=2))
    category = db.Column(db.String())
    order_dishes=db.relationship('Order_Dish', backref='dish', lazy='select')

    def __init__(self, name, description, price, category):
        self.name = name
        self.description = description
        self.price = price
        self.category = category

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Bill(db.Model):
    __tablename__ = 'bill'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DATE)
    orders = db.relationship('Order', backref='bill', lazy='select')
                                                                                                    
    def __repr__(self):
        return '<id {}>'.format(self.id)  
                                               
class Order(db.Model):
    __tablename__ = 'torder'

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String())                                             
    master_order_id=db.Column(db.Integer, db.ForeignKey('master_order.id'))
    bill_id=db.Column(db.Integer, db.ForeignKey('bill.id'))
    order_dishes=db.relationship('Order_Dish', backref='order', lazy='select')
                                                
    def __init__(self, note, master_order_id):
        self.note = note
        self.master_order_id = master_order_id
        self.bill_id = None
                                                
    def __repr__(self):
        return '<id {}>'.format(self.id)   

class Order_Dish(db.Model):
    __tablename__ = 'order_dish'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)                                             
    order_id=db.Column(db.Integer, db.ForeignKey('torder.id'))                                           
    dish_id=db.Column(db.Integer, db.ForeignKey('dish.id'))
                                                   
    def __init__(self, quantity, order_id, dish_id):
        self.quantity = quantity
        self.order_id = order_id
        self. dish_id = dish_id      
                                                
    def __repr__(self):
        return '<id {}>'.format(self.id)

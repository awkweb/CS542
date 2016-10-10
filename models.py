from sqlalchemy.dialects.postgresql import JSON
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

    def __init__(self, d_name, d_desc, d_cost, category, spicy_level, time_to_cook):
        self.d_name = d_name
        self.d_desc = d_desc
        self.d_cost = d_cost
        self.category = category
        self.spicy_level = spicy_level
        self.time_to_cook = time_to_cook

    def __repr__(self):
        return '<id {}>'.format(self.id)

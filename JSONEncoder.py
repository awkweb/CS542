from flask.json import JSONEncoder
from models import *

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promotion):
            return { \
                'id':obj.id, \
                'discount': obj.discount, \
                'description': obj.description, \
                'start_date': obj.start_date, \
                'end_date': obj.end_date \
        	}
        elif isinstance(obj, Bill):
            return { \
                'id':obj.id, \
                'ttl_cost': obj.ttl_cost, \
                'prom_id': obj.prom_id, \
                'pay_id': obj.pay_id \
            }
        elif isinstance(obj, Seating):
            return { \
                'id':obj.id, \
                'table_no': obj.table_no, \
                'seat_no': obj.seat_no, \
            }
        elif isinstance(obj, Dish):
            return { \
                'id':obj.id, \
                'name': obj.name, \
                'description': obj.description, \
                'cost': obj.cost, \
                'category': obj.category, \
                'spicy_level': obj.spicy_level \
            }
        elif isinstance(obj, Employee):
            return { \
                'id':obj.id, \
                'first': obj.first, \
                'last': obj.last, \
                'address': obj.address, \
                'phone': obj.phone, \
                'email': obj.email, \
                'city': obj.city, \
                'state': obj.state, \
                'zipcode': obj.zipcode 
            }
        elif isinstance(obj, Order_Dish):
            return { \
                'id':obj.id, \
                'qty': obj.first, \
                'order_id': obj.order_id, \
                'dish_id': obj.dish_id \
            }
        elif isinstance(obj, Orders):
            return { \
                'id': obj.id, \
                'date': obj.date, \
                'status': obj.status, \
                'note': obj.note, \
                'seat_id': obj.seat_id, \
                'employee_id': obj.employee_id, \
                'bill_id': obj.bill_id \
            }

        return super(MyJSONEncoder, self).default(obj)
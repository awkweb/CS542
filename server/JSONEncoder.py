from flask.json import JSONEncoder
from models import *

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MasterOrder):
        	return { \
                'id':obj.id, \
                'date': obj.date, \
                'status': obj.status, \
            }
        elif isinstance(obj, Bill):
            return { \
                'id':obj.id, \
                'date': obj.date \
            }
        elif isinstance(obj, Dish):
            return { \
                'id':obj.id, \
                'name': obj.name, \
                'description': obj.description, \
                'price': obj.price, \
                'category': obj.category \
            }
        elif isinstance(obj, Order_Dish):
            return { \
                'id':obj.id, \
                'quantity': obj.quantity, \
                'order_id': obj.order_id, \
                'dish_id': obj.dish_id \
            }
        elif isinstance(obj, Order):
            return { \
                'id': obj.id, \
                'note': obj.note, \
                'master_order_id': obj.master_order_id, \
                'bill_id': obj.bill_id \
            }

        return super(MyJSONEncoder, self).default(obj)
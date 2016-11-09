from flask.json import JSONEncoder
from models import *

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MasterOrder):
        	return { \
                'id':obj.id \
            }
        elif isinstance(obj, Bill):
            return { \
                'id':obj.id \
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
        elif isinstance(obj, Order_Dish):
            return { \
                'id':obj.id, \
                'qty': obj.qty, \
                'order_id': obj.order_id, \
                'dish_id': obj.dish_id \
            }
        elif isinstance(obj, Order):
            return { \
                'id': obj.id, \
                'date': obj.date, \
                'status': obj.status, \
                'note': obj.note, \
                'master_order_id': obj.master_order_id, \
                'bill_id': obj.bill_id \
            }

        return super(MyJSONEncoder, self).default(obj)
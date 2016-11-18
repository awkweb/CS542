import json
import os
import time
from flask import Flask, Response, request, render_template, jsonify, json
from models import db
from JSONEncoder import *

app = Flask(__name__, static_url_path='', static_folder='static')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.json_encoder = MyJSONEncoder
db.init_app(app)

from models import *
from exceptions import *
from datetime import datetime


# ERROR AND EXCEPTION HANDLERS 
@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.errorhandler(CustomException)
def handleNotFound(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


# MASTER_ORDER METHODS
@app.route('/api/masterorder/add', methods=['POST'])
def add_master_order():
	if request.method == 'POST':
		masterOrder = MasterOrder()
		db.session.add(masterOrder)
		db.session.commit()
		return jsonify(masterOrder)
	else:
		return not_found()

@app.route('/api/masterorder', methods=['GET'])
def get_master_order():
	id = request.args.get('id')
	if request.method == 'GET':
		if id is not None:
			master_order = MasterOrder.query.get(id)
			if master_order is not None:
				return jsonify(master_order)
		else:
			raise CustomException('Master order was not found.', 404)
	else:
		return not_found()

@app.route('/api/masterorder/all', methods=['GET'])
def get_master_order_all():
	if request.method == 'GET':
		master_orders = MasterOrder.query.all()
		if not master_orders:
			raise CustomException('There are no master orders.', 404)
		return jsonify(master_orders);
	else:
		return not_found()


# ORDER_DISH METHODS
@app.route('/api/orderdish/add', methods=['POST'])
def add_order_dish():
	if request.method == 'POST':
		orderJson = request.get_json(force=True)
		quantity = int(orderJson['quantity'])

		dish_id = int(orderJson['dish_id'])
		dish = Dish.query.get(dish_id)

		order_id = int(orderJson['order_id'])
		order = Order.query.get(order_id)

		if not dish:
			raise CustomException('Dish does not exist.', 404)
		if not order:
			raise CustomException('Order does not exist.', 404)
		if quantity <= 0:
			raise CustomException('Quantity cannot be less than 1.', 400)
		orderDish = Order_Dish( \
			quantity, \
			order_id, \
			dish_id \
		)
		db.session.add(orderDish)
		db.session.commit()
		return jsonify(orderDish)
	else:
		return not_found()

@app.route('/api/orderdish/<id>/updatequantity/<quantity>', methods=['PUT'])
def update_order_dish_quantity(id, quantity):
	if request.method == 'PUT':
		orderDish = Order_Dish.query.get(id)

		if orderDish is not None:
			orderDish.quantity = quantity
			db.session.commit()
			return '', 204
		else:
			raise CustomException('Order dish was not found.', 404)
	else:
		return not_found()


# ORDERS METHODS
@app.route('/api/order/add', methods=['POST'])
def add_order():
	if request.method == 'POST':
		orderJson = request.get_json(force=True)

		master_order_id = int(orderJson['master_order_id'])
		masterOrder = MasterOrder.query.get(master_order_id)

		if not masterOrder:
			raise CustomException("Master order does not exist.", 404);

		order = Order(orderJson['note'], \
			master_order_id \
		)
		db.session.add(order)
		db.session.commit()
		return jsonify(order)
	else:
		return not_found()

@app.route('/api/order/<orderId>/add/bill/<billId>', methods=['POST'])
def add_order_to_bill(orderId, billId):
	if request.method == 'POST':
		order = Order.query.get(orderId)
		bill = Bill.query.get(billId)
		if not order:
			raise CustomException("Order does not exist.", 404)
		if not bill:
			raise CustomException("Bill does not exist.", 404)
		order.bill_id = bill.id
		db.session.commit()
		return jsonify(order)
	else:
		return not_found()

@app.route('/api/order', methods=['GET'])
def get_order():
	id = request.args.get('id')
	status = request.args.get('status')
	if request.method == 'GET':
		if id is not None:
			order = Order.query.get(id)
			if order is not None:
				return jsonify(order)
		elif status is not None:
			orders = db.session.query(Order).filter_by(status=status).all()
			if orders is not None:
				return jsonify(orders)
			else:
				raise CustomException('Orders in {} were \
					not found'.format(status), 404)
		else:
			raise CustomException('Order was not found.', 404)
	else:
		return not_found()


# BILL METHODS
@app.route('/api/bill/start', methods=['POST'])
def start_bill():
	if request.method == 'POST':
		bill = Bill()
		db.session.add(bill)
		db.session.commit()
		return jsonify(bill)
	else:
		return not_found()


# DISH METHODS 
@app.route('/api/dish/add', methods=['POST'])
def add_dish():
	if request.method == 'POST':
		dishJson = request.get_json(force=True)
		dish = Dish( \
			dishJson['name'], \
			dishJson['description'], \
			float(dishJson['price']), \
			dishJson['category'] \
		)
		db.session.add(dish)
		db.session.commit()
		return jsonify(dish)
	else:
		return not_found()

@app.route('/api/dish/delete', methods=['DELETE'])
def delete_dish():
	id = request.args.get('id')
	if request.method == 'DELETE' and id is not None:
		dish = Dish.query.get(id)
		if dish is not None:
			Dish.query.filter_by(id=id).delete()
			db.session.commit()
			return '', 204
		else:
			raise CustomException('Dish was not found.', 404)
	else:
		return not_found()

@app.route('/api/dish/all', methods=['GET'])
def get_dishes():
	if request.method == 'GET':
		dishes = Dish.query.all()
		if not dishes:
			raise CustomException('There are no dishes.', 404)
		return jsonify(dishes);
	else:
		return not_found()

@app.route('/api/dish', methods=['GET'])
def get_dish():
	id = request.args.get('id')
	category = request.args.get('category')
	if request.method == 'GET':
		if id is not None:
			dish = Dish.query.get(id)
			if dish is not None:
				return jsonify(dish)
		elif category is not None:
			dishes = db.session.query(Dish).filter_by(category=category).all()
			if dishes is not None:
				return jsonify(dishes)
			else:
				raise CustomException('Dishes in {} were \
					not found'.format(category), 404)
		else:
			raise CustomException('Dish was not found.', 404)
	else:
		return not_found()

@app.route('/api/dish/update', methods=['PUT'])
def update_dish():
	id = request.args.get('id')
	if request.method == 'PUT' and id is not None:
		dishJson = request.get_json(force=True)
		dish = Dish.query.get(id)
		if dish is not None:
			dish.name = dishJson['name']
			dish.description = dishJson['description']
			dish.price = dishJson['price']
			dish.category = dishJson['category']
			db.session.commit()
			return jsonify(dish)
		else:
			raise CustomException('Dish was not found.', 404)
	else:
		return not_found()


if __name__ == '__main__':
    app.run()


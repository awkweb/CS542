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

# MASTERORDER METHODS
@app.route('/api/masterorder/add', methods=['POST'])
def addMasterOrder():
	if request.method == 'POST':
		masterOrder = MasterOrder()
		db.session.add(masterOrder)
		db.session.commit()
		return jsonify(masterOrder)
	else:
		return not_found()

# ORDER_DISH METHODS
@app.route('/api/orderdish/add', methods=['POST'])
def addOrderDish():
	if request.method == 'POST':
		odJson = request.get_json(force=True)
		qty = int(odJson['qty'])

		dish_id = int(odJson['dish_id'])
		dish = Dish.query.get(dish_id)

		order_id = int(odJson['order_id'])
		order = Order.query.get(order_id)

		if not dish:
			raise CustomException('Dish does not exist.', 404)
		if not order:
			raise CustomException('Order does not exist.', 404)
		if qty <= 0:
			raise CustomException('Quantity cannot be less than 1.', 400)
		orderDish = Order_Dish( \
			qty, \
			order_id, \
			dish_id \
		)
		db.session.add(orderDish)
		db.session.commit()
		return jsonify(orderDish)
	else:
		return not_found()

@app.route('/api/orderdish/<id>/updateQty/<qty>', methods=['PUT'])
def updateOrderDishQty(id, qty):
	if request.method == 'PUT':
		orderDish = Order_Dish.query.get(id)

		if orderDish is not None:
			orderDish.qty = qty
			db.session.commit()
			return '', 204
		else:
			raise CustomException('Order dish was not found.', 404)
	else:
		return not_found()

# ORDERS METHODS
@app.route('/api/order/add', methods=['POST'])
def addOrder():
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
def addOrderToBill(orderId, billId):
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
def getOrder():
	id = request.args.get('id')
	status = request.args.get('status')
	if request.method == 'GET':
		if id is not None:
			order = Orders.query.get(id)
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
def startBill():
	if request.method == 'POST':
		bill = Bill()
		db.session.add(bill)
		db.session.commit()
		return jsonify(bill)
	else:
		return not_found()

# DISH METHODS 
@app.route('/api/dish/add', methods=['POST'])
def addDish():
	if request.method == 'POST':
		dishJson = request.get_json(force=True)
		dish = Dish( \
			dishJson['name'], \
			dishJson['description'], \
			float(dishJson['cost']), \
			dishJson['category'], \
			int(dishJson['spicy_level']) \
		)
		db.session.add(dish)
		db.session.commit()
		return jsonify(dish)
	else:
		return not_found()

@app.route('/api/dish/delete', methods=['DELETE'])
def deleteDish():
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
def getDishes():
	if request.method == 'GET':
		dishes = Dish.query.all()
		if not dishes:
			raise CustomException('There are no dishes.', 404)
		return jsonify(dishes);
	else:
		return not_found()

@app.route('/api/dish', methods=['GET'])
def getDish():
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
def updateDish():
	id = request.args.get('id')
	if request.method == 'PUT' and id is not None:
		dishJson = request.get_json(force=True)
		dish = Dish.query.get(id)
		if dish is not None:
			dish.name = dishJson['name']
			dish.description = dishJson['description']
			dish.cost = dishJson['cost']
			dish.category = dishJson['category']
			dish.spicy_level = dishJson['spicy_level']
			db.session.commit()
			return jsonify(dish)
		else:
			raise CustomException('Dish was not found.', 404)
	else:
		return not_found()


if __name__ == '__main__':
    app.run()

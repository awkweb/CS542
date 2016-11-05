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


# ORDER_DISH METHODS
@app.route('/api/orderdish/add', methods=['POST'])
def addOrderDish():
	if request.method == 'POST':
		odJson = request.get_json(force=True)
		qty = int(odJson['qty'])
		if qty <= 0:
			raise CustomException('Quantity cannot be less than 1.', 400)
		orderDish = Order_Dish( \
			qty, \
			int(odJson['order_id']), \
			int(odJson['dish_id']) \
		)
		db.session.add(orderDish)
		db.session.commit()
		return orderDish.toJSON()
	else:
		return not_found()

@app.route('/api/orderdish/<id>/increase', methods=['PUT'])
def increaseOrderDish(id):
	if request.method == 'PUT':
		orderDish = Order_Dish.query.get(id)
		if orderDish is not None:
			orderDish.qty += 1
			db.session.commit()
		else:
			raise CustomException('Order dish was not found.', 404)
	else:
		return not_found()

@app.route('/api/orderdish/<id>/decrease', methods=['PUT'])
def decreaseOrderDish(id):
	if request.method == 'PUT':
		orderDish = Order_Dish.query.get(id)
		if orderDish is not None:
			if orderDish.qty > 2:
				orderDish.qty -= 1
				db.session.commit()
			else:
				raise CustomException('Quantity cannot be less than 1.', 400)
		else:
			raise CustomException('Order dish was not found.', 404)
	else:
		return not_found()


# ORDERS METHODS
@app.route('/api/orders/add', methods=['POST'])
def addOrder():
	if request.method == 'POST':
		orderJson = request.get_json(force=True)
		order = Orders(None, \
			int(orderJson['seat_id']), \
			int(orderJson['employee_id']), \
			int(orderJson['bill_id']) \
		)
		db.session.add(order)
		db.session.commit()
		return jsonify(order)
	else:
		return not_found()

@app.route('/api/orders', methods=['GET'])
def getOrder():
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
@app.route('/api/bills/start', methods=['POST'])
def startBill():
	if request.method == 'POST':
		bill = Bill()
		db.session.add(bill)
		db.session.commit()
		return jsonify(bill)
	else:
		return not_found()

@app.route('/api/bills/<id>/promotions/<promoId>', methods=['PUT'])
def addPromotionToBill(id, promoId):
	if request.method == 'PUT':
		bill = Bill.query.get(id)

		if bill is None:
			raise CustomException('Bill was not found.', 404)

		promotion = Promotion.query.get(promoId)
		if promotion is None:
			raise CustomException('Promotion was not found.', 404)

		today = datetime.today().date()
		if (today >= promotion.start_date and \
			today <= promotionstion.end_date):
			bill.prom_id = promotion.id
			db.session.commit()
			return jsonify(bill)
		else:
			raise CustomException("Promotion has expired.", 400)

	else:
		return not_found()


# PROMOTION METHODS
@app.route('/api/promotions/add', methods=['POST'])
def addPromotion():
	if request.method == 'POST':
		promotionJson = request.get_json(force=True)
		start_date = datetime.strptime(promotionJson['start_date'] , '%Y-%m-%d')
		end_date = datetime.strptime(promotionJson['end_date'] , '%Y-%m-%d')
		if end_date < start_date:
			raise CustomException('End date of promotion cannot be \
				before start date of promotion.', 400)
		promotion = Promotion( \
			float(promotionJson['discount']), \
			promotionJson['description'], \
			start_date, \
			end_date \
		)
		db.session.add(promotion)
		db.session.commit()
		return jsonify(promotion)
	else:
		return not_found()

@app.route('/api/promotions', methods=['GET'])
def getPromotion():
	id = request.args.get('id')
	if request.method == 'GET':
		if id is not None:
			promotion = Promotion.query.get(id)
			if promotion is not None:
				return jsonify(promotion)
			else:
				return CustomException("Promotion was not found.", 404)
		else:
			promotions = Promotion.query.all()
			return jsonify(promotions)
	else:
		return not_found()

@app.route('/api/promotions/delete/expired', methods=['DELETE'])
def deletePromotion():
	if request.method == 'DELETE':
		today = datetime.today().date()
		promotions = Promotion.query.filter( \
			Promotion.end_date < today).delete()
		db.session.commit()
		return '', 204
	else:
		return not_found()


# SEATING METHODS
@app.route('/api/seating/add', methods=['POST'])
def addSeating():
	if request.method == 'POST':
		seatingJson = request.get_json(force=True)
		seating = Seating( \
			int(seatingJson['table_no']), \
			int(seatingJson['seat_no']) \
			)
		db.session.add(seating)
		db.session.commit()
		return jsonify(seating)
	else:
		return not_found()

@app.route('/api/seating', methods=['GET'])
def getSeating():
	id = request.args.get('id')
	if request.method == 'GET' and id is not None:
		seating = Seating.query.get(id)
		if seating is not None:
			return jsonify(seating)
		else:
			raise CustomException('Seating was not found.', 404)
	else:
		return not_found()


# DISH METHODS 
@app.route('/api/dishes/add', methods=['POST'])
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

@app.route('/api/dishes/delete', methods=['DELETE'])
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

@app.route('/api/dishes', methods=['GET'])
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

@app.route('/api/dishes/update', methods=['PUT'])
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

# EMPLOYEE METHODS 
@app.route('/api/employees/add', methods=['POST'])
def addEmployee():
	if request.method == 'POST':
		empJson = request.get_json(force=True)
		employee = Employee( \
			empJson['first'], \
			empJson['last'], \
			empJson['address'], \
			empJson['phone'], \
			empJson['email'], \
			empJson['city'], \
			empJson['state'], \
			empJson['zipcode'] \
		)
		db.session.add(employee)
		db.session.commit()
		return jsonify(employee)
	else:
		return not_found()

@app.route('/api/employees/delete', methods=['DELETE'])
def deleteEmployee():
	id = request.args.get('id')
	if request.method == 'DELETE' and id is not None:
		employee = Employee.query.get(id)
		if employee is not None:
			Employee.query.filter_by(id=id).delete()
			db.session.commit()
			return '', 204
		else:
			raise CustomException('Employee was not found.', 404)
	else:
		return not_found()

@app.route('/api/employees', methods=['GET'])
def getEmployee():
	id = request.args.get('id')
	if request.method == 'GET' and id is not None:
		employee = Employee.query.get(id)
		if employee is not None:
			return jsonify(employee)
		else:
			raise CustomException('Employee was not found.', 404)
	else:
		return not_found()


if __name__ == '__main__':
    app.run()

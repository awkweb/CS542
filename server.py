import json
import os
import time
from flask import Flask, Response, request, render_template, jsonify, json
from models import db

app = Flask(__name__, static_url_path='', static_folder='dist')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from models import *
from exceptions import *

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

@app.route('/dish/add', methods=['POST'])
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
		return dish.toJSON()
	else:
		return not_found()

@app.route('/dish/delete', methods=['DELETE'])
def deleteDish():
	id = request.args.get('id')
	if request.method == 'DELETE' and id is not None:
		dish = Dish.query.filter_by(id=id).first()
		if dish is not None:
			Dish.query.filter_by(id=id).delete()
			db.session.commit()
			return '', 204
		else:
			raise CustomException('Dish was not found.', 404)
	else:
		return not_found()

@app.route('/dish', methods=['GET'])
def getDish():
	id = request.args.get('id')
	if request.method == 'GET' and id is not None:
		dish = Dish.query.filter_by(id=id).first()
		if dish is not None:
			return dish.toJSON()
		else:
			raise CustomException('Dish was not found.', 404)
	else:
		return not_found()

@app.route('/employee/add', methods=['POST'])
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
		return employee.toJSON()
	else:
		return not_found()

@app.route('/employee/delete', methods=['DELETE'])
def deleteEmployee():
	id = request.args.get('id')
	if request.method == 'DELETE' and id is not None:
		employee = Employee.query.filter_by(id=id).first()
		if employee is not None:
			Employee.query.filter_by(id=id).delete()
			db.session.commit()
			return '', 204
		else:
			raise CustomException('Employee was not found.', 404)
	else:
		return not_found()

@app.route('/employee', methods=['GET'])
def getEmployee():
	id = request.args.get('id')
	if request.method == 'GET' and id is not None:
		employee = Employee.query.filter_by(id=id).first()
		if employee is not None:
			return employee.toJSON()
		else:
			raise CustomException('Employee was not found.', 404)
	else:
		return not_found()


if __name__ == '__main__':
    app.run()
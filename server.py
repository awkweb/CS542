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
from manager import *

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/employee/add', methods=['POST'])
def hello():
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


if __name__ == '__main__':
    app.run()
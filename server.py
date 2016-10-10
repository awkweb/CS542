import json
import os
import time
from flask import Flask, Response, request
from models import db

app = Flask(__name__, static_url_path='', static_folder='dist')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from models import Dish

@app.route('/api/dishes', methods=['GET'])
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3000)))
import json
import os
import time
from flask import Flask, Response, request

app = Flask(__name__, static_url_path='', static_folder='dist')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))


@app.route('/api/dishes', methods=['GET'])
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3000)), debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime
from db.index import init_app


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

init_app(app)


@app.route('/',methods=["GET"])
def hello():
    name = request.args.get("name", "world")
    return 'Hello'


if __name__ == '__main__':
    app.run()
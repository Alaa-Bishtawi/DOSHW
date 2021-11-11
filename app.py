import sqlite3
from flask import Flask, request
import json
import requests as requests
from flask.wrappers import Response
from werkzeug.wrappers import response
app = Flask(__name__)

catalog_server = "http://192.168.1.129:3000"
order_server = "http://192.168.1.129:5000"


@app.route('/items', methods=['GET'])
def query_by_item_search():
    response = requests.get(url=catalog_server+"/items")
    return response


@app.route('/search/topic', methods=['GET'])
def query_by_subject_search():
    topic_name = request.args.get("name")
    response = requests.get(url=catalog_server+"/topic", params=topic_name)
    return response


@app.route('/search/itemnumber', methods=['GET'])
def search_by_item_number():
    item_number = request.args.get("item_number")
    response = requests.get(
        url=catalog_server+"/itemnumber", params=item_number)
    return response


@app.route('/update/stock', methods=['GET'])
def update_stock():
    id_item = request.args.get("book_id")
    stock_avilable_number = request.args.get("stock")
    response = requests.get(
        url=catalog_server+"/update/stock", params={id_item, stock_avilable_number})
    return response


@app.route('/update/cost', methods=['GET'])
def update_cost():
    id_item = request.args.get("book_id")
    cost = request.args.get("cost")


@app.route('/purchase', methods=['GET'])
def purchase():
    item_number = request.args.get("item_number")
    response = requests.get(url=order_server+"/purchase", params=item_number)
    return response


@app.route('/')
def hello_world():
    x = {
        "stock": True
    }
    y = json.dumps(x)
    return y


if __name__ == '__main__':
    app.run()

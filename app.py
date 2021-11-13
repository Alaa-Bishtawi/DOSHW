import sqlite3
from flask import Flask, request
import json
import requests as requests
app = Flask(__name__)

catalog_server = "http://192.168.56.103:5000"
order_server = "http://192.168.56.104:5000"

# just normal pass-through of the requests to the other servcies


@app.route('/search/topic', methods=['GET'])
def query_by_subject_search():
    topic_name = request.args.get("name")
    response = requests.get(
        url=catalog_server+"/search/topic", params={"name": topic_name})
    return response.json()


@app.route('/search/itemnumber/', methods=['GET'])
def search_by_item_number():
    item_number = request.args.get("item_number")
    response = requests.get(
        url=catalog_server+"/search/itemnumber", params={"item_number": item_number})
    return response.json()


@app.route('/update/stock', methods=['PATCH'])
def update_stock():
    id_item = request.args.get("item_number")
    stock = request.args.get("stock")
    response = requests.get(
        url=catalog_server+"/update/stock", params={"item_number": id_item, "stock": stock})
    return response.json()


@app.route('/update/cost', methods=['PATCH'])
def update_cost():
    id_item = request.args.get("item_number")
    cost = request.args.get("cost")
    response = requests.get(

        url=catalog_server+"/update/cost", params={"item_number": id_item, "cost": cost})
    return response.json()


@app.route('/purchase', methods=['POST'])
def purchase():
    item_number = request.args.get("item_number")
    response = requests.get(url=order_server+"/purchase",
                            params={"item_number": item_number})
    return response.json()


@app.route('/')
def hello_world():
    return "front end is working ..."


if __name__ == '__main__':
    app.run(port=7000)

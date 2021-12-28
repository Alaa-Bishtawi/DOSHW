import sqlite3
import json
from flask import Flask, request
from http import HTTPStatus
import requests
app = Flask(__name__)


catalog_server_1 = "http://127.0.0.1:5001"
catalog_server_2 = "1"
order_server_1 = "1"
order_server_2 = "1"

catalog_server_1_stock = []
catalog_server_2_stock = []
catalog_server_1_cost = []
catalog_server_2_cost = []
order_server_1_q = []
order_server_2_q = []


catalog_server = "http://192.168.56.103:5000"
order_server = "http://192.168.56.104:5000"
loadbalance_flag = True
read_cache = dict()


def cache_put(key, value):
    read_cache[key] = value


def cache_get(key):
    return read_cache.get(key)


def cache_pop(key):
    read_cache.pop(key)


# just simple forwarding of the request of the request to the other servcies
@app.route('/search/topic', methods=['GET'])
def query_by_subject_search():
    global loadbalance_flag
    topic_name = request.args.get("name")
    cache = cache_get("topic"+topic_name)
    print(cache_get("topic"+topic_name))
    if cache == None:
        if loadbalance_flag == True:
            
            loadbalance_flag = False
            try:
                response = requests.get(
                    url=catalog_server_1+"/search/topic", params={"name": topic_name})
            except:
                response = requests.get(
                    url=catalog_server_2+"/search/topic", params={"name": topic_name})
        else :
            
            loadbalance_flag = True
            try:
                response = requests.get(
                    url=catalog_server_2+"/search/topic", params={"name": topic_name})
            except:
                response = requests.get(
                    url=catalog_server_1+"/search/topic", params={"name": topic_name})
        cache_put("topic"+topic_name, response.json())
        return response.json()
    else:
        return cache


@app.route('/search/itemnumber/', methods=['GET'])
def search_by_item_number():
    global loadbalance_flag
    item_number = request.args.get("item_number")
    cache = cache_get("book"+item_number)
    if cache == None:
        if loadbalance_flag == True:
            
            loadbalance_flag = False
            try:
                response = requests.get(
                    url=catalog_server_1+"/search/itemnumber", params={"item_number": item_number})
            except:
                response = requests.get(
                    url=catalog_server_2+"/search/itemnumber", params={"item_number": item_number})
        else :
            
            loadbalance_flag = True
            try:
                response = requests.get(
                    url=catalog_server_2+"/search/itemnumber", params={"item_number": item_number})
            except:
                response = requests.get(
                    url=catalog_server_1+"/search/itemnumber", params={"item_number": item_number})
        cache_put("book"+item_number, response.json())
        return response.json()
    else:
        return cache


@app.route('/update/stock', methods=['PATCH'])
def update_stock():
    id_item = request.args.get("item_number")
    stock = request.args.get("stock")
    try:
        url = catalog_server_1+"/update/stock"
        params = {"item_number": id_item, "stock": stock}
        response = requests.patch(url=url, params=params)
        print(response)
        return response.json()
    except:
        catalog_server_1_stock.append({"url": url, "params": params})
    try:
        url = catalog_server_2+"/update/stock"
        params = {"item_number": id_item, "stock": stock}
        response = requests.patch(url=url, params=params)
        print(response)
        return response.json()
    except:
        catalog_server_2_stock.append({"url": url, "params": params})
    return "200"


@app.route('/update/cost', methods=['PATCH'])
def update_cost():
    id_item = request.args.get("item_number")
    cost = request.args.get("cost")
    try:
        url = catalog_server_1+"/update/cost"
        params = {"item_number": id_item, "cost": cost}
        response = requests.patch(url=url, params=params)
        print(response)
        return response.json()
    except:
        catalog_server_1_cost.append({"url": url, "params": params})
    try:
        url = catalog_server_2+"/update/cost"
        params = {"item_number": id_item, "cost": cost}
        response = requests.patch(url=url, params=params)
        print(response)
        return response.json()
    except:
        catalog_server_2_cost.append({"url": url, "params": params})
    print(catalog_server_1_cost)
    return "200"
    


@app.route('/purchase', methods=['POST'])
def purchase():
    item_number = request.args.get("item_number")
    try:
        url = order_server_1+"/purchase"
        params = {"item_number": item_number}
        response = requests.post(url, params)
    except:
        order_server_1_q.append({"url": url, "params": params})
    try:
        url = order_server_2+"/purchase"
        params = {"item_number": item_number}
        response = requests.post(url, params)
    except:
        order_server_2_q.append({"url": url, "params": params})
    return response.json()


@app.route('/serverup', methods=['GET'])
def serverup():
    server_name = request.args.get("server_name")
    server_number = request.args.get("server_number")
    try:
        if server_name == "catalog":
            if server_number == "1":
                if len(catalog_server_1_cost) > 0:
                    for x in catalog_server_1_cost:
                        response = requests.patch(
                            x["url"], x["params"])
                    catalog_server_1_cost.clear()
                if len(catalog_server_1_stock) > 0:
                    for x in catalog_server_1_stock:
                        response = requests.patch(
                            x["url"], x["params"])
                    catalog_server_1_stock.clear()
            elif server_number == "2":
                if len(catalog_server_2_cost) > 0:
                    for x in catalog_server_2_cost:
                        response = requests.patch(
                            x["url"], x["params"])
                    catalog_server_2_cost.clear()
                if len(catalog_server_2_stock) > 0:
                    for x in catalog_server_2_stock:
                        response = requests.patch(
                            x["url"], x["params"])
                    catalog_server_2_stock.clear()
        if server_name == "order":
            if server_number == "1":
                if len(order_server_1_q) > 0:
                    for x in order_server_1_q:
                        response = requests.patch(
                            x["url"], x["params"])
                    order_server_1_q.clear()
            elif server_number == "2":
                if len(order_server_2_q) > 0:
                    for x in order_server_2_q:
                        response = request.get(
                            x["url"], x["params"])
                    order_server_1_q.clear()
        return json.dumps({
        "status": HTTPStatus.OK
    })
        
    except:
        return "server up problem"


@app.route('/')
def hello_world():
    return "front end is working..."


@app.route('/cache', methods=["DELETE"])
def cache_invalidate():
    cache_key = request.args.get("key")
    if cache_get(cache_key) != None:
        cache_pop(cache_key)
        return "200"
    else:
        return "404"


if __name__ == '__main__':
    print("a")
    app.run(port=5000)

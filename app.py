from http import HTTPStatus
import requests as requests
from flask import Flask, request
import json
app = Flask(__name__)

catalog_server_ip = "http://192.168.56.103:5000"

# take path variable (item_number) as int to make a purchase


@app.route('/purchase', methods=['POST'])
def purchase():
    item_number = request.args.get("item_number")

    success = {
        "purchase_status": "Sucessful"+" item_number:"+item_number,
        "status": HTTPStatus.OK
    }
    fails = {
        "purchase_status": "No Stock"+" item_number:"+item_number,
        "status": HTTPStatus.OK
    }
    success = json.dumps(success)
    fails = json.dumps(fails)
    stock_check = requests.get(
        url=catalog_server_ip+"/check", params={"item_number": item_number})
    stock_check_json = stock_check.json()
    if stock_check_json["stock_check"] == True:
        requests.get(
            url=catalog_server_ip+"/update/stock/dec", params={"item_number": item_number})
        return success
    else:
        return fails


@app.route('/')
def hello_world():
    return 'Hello World! working ORDER SERVER'


if __name__ == '__main__':
    app.run()

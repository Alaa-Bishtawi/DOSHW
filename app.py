from http import HTTPStatus
import requests as requests
from flask import Flask, request
import json
app = Flask(__name__)

catalog_server_ip = "http://192.168.1.129:3000"


@app.route('/purchase', methods=['GET'])
def purchase():
    item_number = request.args.get("item_number")

    success = {
        "purchase_status": "Sucessful",
        "status": HTTPStatus.OK
    }
    fails = {
        "purchase_status": "No Stock",
        "status": HTTPStatus.OK
    }
    success = json.dumps(success)
    fails = json.dumps(fails)
    stock_check = requests.get(
        url=catalog_server_ip+"/check", params=item_number)
    stock_check_json = stock_check.json()
    if stock_check_json['stock'] == True:
        purchase_confirm = requests.get(url=catalog_server_ip +
                                        "/update/stock/dec", params=item_number)
        return success
    else:
        return fails


@app.route('/')
def hello_world():
    return 'Hello World! working ORDER SERVER'


if __name__ == '__main__':
    app.run()

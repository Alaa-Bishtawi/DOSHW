import requests as requests
from flask import Flask, request
import json
app = Flask(__name__)
from http import HTTPStatus
catalog_server_ip = "http://192.168.1.129:3000"
@app.route('/purchase', methods=['GET'])
def purchase():
    success = {
        "purchase_status": "Sucessful",
        "status" : HTTPStatus.OK
    }
    fails ={
        "purchase_status": "No Stock",
        "status": HTTPStatus.OK
    }
    success = json.dumps(success)
    fails = json.dumps(fails)
    item_number = request.args.get("item_number")

    r = requests.get(url=catalog_server_ip+"/check", params=item_number)
    result = r.json()
    if result['stock'] ==True:
        r = requests.get(url=catalog_server_ip + "/purchase/confirm", params=item_number)
        return success
    else:
        return fails
@app.route('/')
def hello_world():
    return 'Hello World! 5000'


if __name__ == '__main__':
    app.run()

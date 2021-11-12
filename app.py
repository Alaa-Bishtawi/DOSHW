import sqlite3
from http import HTTPStatus
from flask import Flask, request
import json
app = Flask(__name__)


@app.route('/search/topic', methods=['GET'])
def query_by_subject_search():
    topic = request.args.get("name")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(f"SELECT topic_id FROM topics WHERE topic_name =  '{topic}';")
    result = cur.fetchone()

    # transfer for json
    cur.execute(f"SELECT * FROM book where topic_id = {result[0]};")
    all_results = cur.fetchall()
    print(all_results)  # transfer to json
    jsonRes = {
        "status": HTTPStatus.OK,
        "items": []

    }
    for item in all_results:
        jsonRes["items"].append(item[0])
    return json.dumps(jsonRes)


@app.route('/search/itemnumber', methods=['GET'])
def query_by_item_search():
    id = request.args.get("id")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM book WHERE book_id =  '{id}';")
    result = cur.fetchone()
    print(result)
    return json.dumps({
        "status": HTTPStatus.OK
    })


@app.route('/update/stock', methods=['GET'])
def update_stock():
    id_item = request.args.get("book_id")
    stock_avilable_number = request.args.get("stock")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(
        f"UPDATE book SET stock_avilable_number = {stock_avilable_number} where book_id={id_item};")
    conn.commit()
    return json.dumps({
        "status": HTTPStatus.OK
    })


@app.route('/update/cost', methods=['GET'])
def update_cost():
    id_item = request.args.get("book_id")
    cost = request.args.get("cost")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(f"UPDATE book SET cost = {cost} where book_id={id_item};")
    conn.commit()
    return json.dumps({
        "status": HTTPStatus.OK
    })


@app.route('/update/cost/dec', methods=['GET'])
def update_cost_dec():
    id_item = request.args.get("book_id")
    cost = request.args.get("cost")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(f"Select cost where book_id={id_item};")
    cost_current = conn.fetch()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE book SET cost = {cost_current-1} where book_id={id_item};")
    conn.commit()
    return json.dumps({
        "status": HTTPStatus.OK
    })


@app.route('/check')
def hello_world():
    # a Python object (dict):
    x = {
        "stock": True
    }
    y = json.dumps(x)
    return y


if __name__ == '__main__':
    app.run(port=9000)

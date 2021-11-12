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
    cur.execute(f"SELECT * FROM book where topic_id = {result[0]};")
    all_results = cur.fetchall()
    print(all_results)  # transfer to json
    jsonRes = {
        "status": HTTPStatus.OK,
        "items": []

    }
    for item in all_results:
        jsonRes["items"].append({"book_id": item[3], "book_name": item[0]})
    return json.dumps(jsonRes)


@app.route('/search/itemnumber', methods=['GET'])
def query_by_item_search():
    id_item = request.args.get("item_number")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM book WHERE book_id =  '{id_item}';")
    result = cur.fetchone()
    print(result)
    return json.dumps({
        "status": HTTPStatus.OK,
        "book_id": result[3],
        "book_name": result[0],
        "cost": result[2],
        "topic": result[4],
        "stock": result[1],

    })


@app.route('/update/stock', methods=['PATCH'])
def update_stock():
    id_item = request.args.get("item_number")
    stock_avilable_number = request.args.get("stock")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(
        f"UPDATE book SET stock_avilable_number = {stock_avilable_number} where book_id={id_item};")
    conn.commit()
    return json.dumps({
        "status": HTTPStatus.OK
    })


@app.route('/update/cost', methods=['PATCH'])
def update_cost():
    id_item = request.args.get("item_number")
    cost = request.args.get("cost")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(
        f"UPDATE book SET cost = {cost} where book_id={id_item};")
    conn.commit()
    return json.dumps({
        "status": HTTPStatus.OK
    })


@app.route('/update/stock/dec', methods=['GET'])
def update_stock_dec():
    id_item = request.args.get("item_number")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(
        f"Select stock_avilable_number FROM book where book_id={id_item};")
    stock_avilable_number_current = cur.fetchone()
    cur = conn.cursor()
    cur.execute(
        f"UPDATE book SET stock_avilable_number = {stock_avilable_number_current[0]-1} where book_id={id_item};")
    conn.commit()
    return json.dumps({
        "status": HTTPStatus.OK
    })


@app.route('/check')
def hello_world():
    id_item = request.args.get("item_number")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(
        f"SELECT stock_avilable_number FROM book WHERE book_id =  '{id_item}';")
    result = cur.fetchone()
    print(result)
    return json.dumps({
        "status": HTTPStatus.OK,
        "stock_check": result[0] > 0 if True else False
    })


if __name__ == '__main__':
    app.run(port=9000)

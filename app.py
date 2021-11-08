import sqlite3

from flask import Flask , request


import json
app = Flask(__name__)
@app.route('/update/stock', methods=['GET'])
def update_stock():
    id = request.args.get("book_id")
    stock_avilable_number = request.args.get("stock")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(f"UPDATE book SET stock_avilable_number = {stock_avilable_number} where book_id={id};")
    conn.commit()


    return ""




@app.route('/update/cost', methods=['GET'])
def update_cost():
    id = request.args.get("book_id")
    cost = request.args.get("cost")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(f"UPDATE book SET cost = {cost} where book_id={id};")
    conn.commit()


    return ""
@app.route('/topic', methods=['GET'])
def query_by_subject_search():
    topic = request.args.get("topic")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(f"SELECT topic_id FROM topics WHERE topic_name =  '{topic}';")
    result = cur.fetchone()
    cur.execute(f"SELECT * FROM book where topic_id = {result[0]};")#transfer for json
    all_results = cur.fetchall()
    print(all_results)#transfer to json
    return ""
@app.route('/item', methods=['GET'])
def query_by_item_search():
    id = request.args.get("id")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM book WHERE book_id =  '{id}';")
    result = cur.fetchone()
    print(result)
    return ""
def update_cost():
    return
def update_stock():
    increaseDecrease = True

@app.route('/itemnumber', methods=['GET'])
def search_by_item_number():
    return
@app.route('/check')
def hello_world():
    # a Python object (dict):
    x = {
        "stock": True
    }
    y = json.dumps(x)
    return y


if __name__ == '__main__':
    app.run()

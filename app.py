import sqlite3
from http import HTTPStatus
from flask import Flask, request
import requests
import json
app = Flask(__name__)

front_server="http://localhost:5000"
server_name="catalog"
server_number="1"
# takes path variable (name) as a string to get back all the items


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

# take path variable (item_number) as a int id to return all relevant data


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

# take 2 path variables (item_number,stock) as ints to update stock


@app.route('/update/stock', methods=['PATCH'])
def update_stock():
    id_item = request.args.get("item_number")
    stock_avilable_number = request.args.get("stock")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(
        f"UPDATE book SET stock_avilable_number = {stock_avilable_number} where book_id={id_item};")
    
    requests.delete(url=front_server+"/cache",params={"key":"book"+id_item})
    cur.execute(f"SELECT topic_id FROM book where book_id = {id_item};")
    results = cur.fetchone()
    cur.execute(f"SELECT topic_name FROM topic where topic_id = {results[0]};")
    results = cur.fetchone()
    conn.commit()
    requests.delete(url=front_server+"/cache",params={"key":"topic"+str(results[0])})
    
    return json.dumps({
        "status": HTTPStatus.OK
    })

# take 2 path variables (item_number,cost) as ints to update cost


@app.route('/update/cost', methods=['PATCH'])
def update_cost():
    id_item = request.args.get("item_number")
    cost = request.args.get("cost")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(f"UPDATE book SET cost = {cost} where book_id={id_item};")
    cur.execute(f"SELECT topic_id FROM book where book_id = {id_item};")
    results = cur.fetchone()
    conn.commit()
    requests.delete(url=front_server+"/cache",params={"key":"book"+id_item})
    print(results)
    requests.delete(url=front_server+"/cache",params={"key":"topic"+str(results[0])})
    
    return json.dumps({
        "status": HTTPStatus.OK
    })


# take path variable (item_number) as ints to dec stock by 1 after purchase
@app.route('/update/stock/dec', methods=['POST'])
def update_stock_dec():
    id_item = request.args.get("item_number")
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(f"Select stock_avilable_number FROM book where book_id={id_item};")
    stock_avilable_number_current = cur.fetchone()
    cur = conn.cursor()
    cur.execute(f"UPDATE book SET stock_avilable_number = {stock_avilable_number_current[0]-1} where book_id={id_item};")
    conn.commit()
    requests.delete(url=front_server+"/cache",params={"key":"book"+id_item})
    return json.dumps({
        "status": HTTPStatus.OK
    })

# take path variable (item_number) as int to check stock


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

@app.route('/up')
def up():
    requests.get(url=front_server,params={"server_name":server_name,"server_number":server_number})


if __name__ == '__main__':
    app.run(port=9000)

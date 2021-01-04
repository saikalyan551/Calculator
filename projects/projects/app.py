import sqlite3
import json
from flask import Flask, jsonify, request, render_template, g
from flask.cli import with_appcontext
import os

app = Flask(__name__)

pwd = os.path.dirname(os.path.abspath(__file__))

class FileItem(dict):
    def __init__(self, fname):
        dict.__init__(self, fname=fname)

@app.route("/")
def home():
    connection = sqlite3.connect("calculator_logs.db") #db initializing
    cursor = connection.cursor()                #cursor to query the db 
    query = "SELECT logs from calculator_logs" #Sql Query
    result = cursor.execute(query) # store result in result
    result = result.fetchall()  #get all values
    result = result[::-1] 
    result = result[0:10]
    final_result = []
    for i in result:
        i= str(i).replace(",","").replace("(","").replace(")","").replace("'","")
        final_result.append(i)
    return render_template("HTML/index.html",result=final_result)


@app.route('/compute', methods=['GET', 'POST'])
def testfn():
    # GET request
    if request.method == 'GET':
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers
    # POST request
    if request.method == 'POST':
        value = request.get_json()
        value = value["expression"]
        connection = sqlite3.connect("calculator_logs.db")
        cursor = connection.cursor()
        query1 = "INSERT INTO calculator_logs VALUES('{logs}')".format(logs=value)
        cursor.execute(query1)
        connection.commit()
        return 200


app.run(host='0.0.0.0', debug=True, port=5000)

from flask import request
from flask import jsonify
from app import app

from app import db_conn

@app.route('/cmd/<user_id>', methods = ['POST', 'GET'])
def cmd(user_id):
    if request.method == "POST": 
        return writeCommands(request, user_id)
    elif request.method == 'GET':
        return readCommands(user_id)

def readCommands(user_id):
    commands = db_conn.getCommands(user_id)
    return jsonify(commands), 200
    
def writeCommands(request, user_id):
    csv_data = request.data.decode('utf-8')  # Assuming the data is encoded as UTF-8
    csv_lines = csv_data.split('\n')  # Split the data into lines

    row = []
    counter = 0
    cmd = ""
    start_time = ""
    exit_code = ""
    execution_time = ""

    # Iterate over each line and parse it as CSV
    for line in csv_lines:
        if counter == 0:
            cmd = line
            counter = 1
        elif counter == 1:
            start_time = line
            counter = 2
        elif counter == 2:
            exit_code = line
            counter = 3
        elif counter == 3:
            execution_time = line
            counter = 0
            row.append({
                "command": cmd,
                "start_time": start_time,
                "exit_code": exit_code,
                "execution_time": execution_time,
                "user_id": user_id,
            })

    db_conn.writeCommandsToDb(row)
    return jsonify({"message": "OK"}), 200
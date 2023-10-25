from flask import Flask
from flask import request
from flask import jsonify, make_response

import mysql.connector

import datetime
import os

connStrTpl = "mysql+pymysql://{0}:{1}@{2}/{3}"
dbUser = os.environ["DB_USER"]
dbPwd = os.environ["DB_PASSWORD"]
dbAddress = os.environ["DB_ADDR"]
dbDB = os.environ["DB_DATABASE"]

connStr = connStrTpl.format(dbUser, dbPwd, dbAddress, dbDB)

creation = "CREATE TABLE IF NOT EXISTS `commands` ( `ID` INT NOT NULL AUTO_INCREMENT, `CommandBody` VARCHAR(255), `StartTime` DATETIME NOT NULL, `TimeElapsedInSec` INT NOT NULL, `ExitCode` INT NOT NULL, `UserId` VARCHAR(255) NOT NULL, KEY `ExitCodeIndex` (`ExitCode`) USING BTREE, PRIMARY KEY (`ID`) );"
insertion = "INSERT INTO commands (CommandBody, StartTime, TimeElapsedInSec, ExitCode, UserId) VALUES (%s, %s, %s, %s, %s)"

config = {
        'user': dbUser,
        'password': dbPwd,
        'host': dbAddress.split(":")[0],
        'port': dbAddress.split(":")[1],
        'database': dbDB,
    }
connection = mysql.connector.connect(**config)
c = connection.cursor()
c.execute(creation)
c.close()

app = Flask(__name__)

@app.route('/healthz')
def healthz():
    response = make_response("OK", 200)
    response.mimetype = "text/plain"
    return response

@app.route('/cmd/<user_id>', methods = ['POST'])
def cmd(user_id):
    if request.method == "POST": 
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

        writeCommandsToDb(row)
        
        return jsonify({"message": "OK"}), 200

def writeCommandsToDb(rows):
    print("successfully connect to database")
    cursor = connection.cursor()
    for row in rows:
        timestamp = datetime.datetime.fromtimestamp(int(row['start_time']))
        start = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(insertion, (row['command'], start, row['execution_time'], row['exit_code'], row['user_id']))
    connection.commit()
    cursor.close()
    print("successfully insert data")

if __name__ == '__main__':
    port = os.environ["PORT"]
    app.run(debug=True, host='0.0.0.0', port=port)
from flask import Flask
from flask import request
from flask import jsonify, make_response

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
import datetime
import os

connStrTpl = "mysql://{0}:{1}@{2}/{3}"
dbUser = os.environ["DB_USER"]
dbPwd = os.environ["DB_PASSWORD"]
dbAddress = os.environ["DB_ADDR"]
dbDB = os.environ["DB_DATABASE"]

connStr = connStrTpl.format(dbUser, dbPwd, dbAddress, dbDB)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = connStr
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

insertion = "INSERT INTO commands (CommandBody, StartTime, TimeElapsedInSec, ExitCode) VALUES (%s, %s, %s, %s)"

class Command(db.Model):
    __tablename__ = 'commands'
    id = db.Column(db.Integer, primary_key=True)
    commandBody = db.Column(db.String(255))
    startTime = db.Column(db.DateTime)
    timeElapsedInSec = db.Column(db.Integer)
    exitCode = db.Column(db.Integer, index=True)
    userId = db.Column(db.String(255), index=True)

    def __repr__(self):
        return '<Command %r>' % self.name

@app.route('/healthz')
def healthz():
    response = make_response("OK", 200)
    response.mimetype = "text/plain"
    return response

@app.route('/cmd/<user_id>', methods = ['POST'])
def cmd(session):
    if request.method == "POST": 
        user_id = request.view_args["user_id"]
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
    for row in rows:
        timestamp = datetime.datetime.fromtimestamp(int(row['start_time']))
        start = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        db.session.add(Command(commandBody = row['command'],
                            startTime = start,
                            exitCode = row['exit_code'],
                            timeElapsedInSec = row['execution_time'],
                            userId = row['user_id']))
    db.session.commit()
    print("successfully insert data")

if __name__ == '__main__':
    port = os.environ["PORT"]
    app.run(debug=True, host='0.0.0.0', port=port)
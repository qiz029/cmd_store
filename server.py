from flask import Flask
from flask import request

app = Flask(__name__)

class command:
    def __init__(self, cmd, start_time, exit_code, execution_time):
        self.cmd = cmd
        self.start_time = start_time
        self.exit_code = exit_code
        self.execution_time = execution_time

    def to_dict(self):
        return {
            "command": self.cmd,
            "start_time": self.start_time,
            "exit_code": self.exit_code,
            "execution_time": self.execution_time,
        }

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/cmd/<session>', methods = ['POST'])
def cmd(session):
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
                })

        # TODO: write this into elastic search.
        
        return 'OK', 200

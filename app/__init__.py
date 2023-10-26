from flask import Flask, make_response
import os

app = Flask(__name__)

@app.route('/healthz')
def healthz():
    response = make_response("OK", 200)
    response.mimetype = "text/plain"
    return response

from app import cmd_handler

port = os.environ["PORT"]
app.run(debug=True, host='0.0.0.0', port=port)
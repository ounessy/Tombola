from flask import Flask, request
from process import process
from datetime import datetime

from utils import *
import subprocess



app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/test", methods=["POST", "GET"])
def test():
    subprocess.Popen(r"E:\OMOTombola\Webservice2\naps2\App\naps2.console -o E:\OMOTombola\Webservice2\scans\2021-10-10_18-55-23-751638.pdf -f", shell = True)
    return "aa"

@app.route("/processData", methods=["POST", "GET"])
def processData():
    time = str(datetime.now())
    data=request.form.to_dict()
    savingStatus = saveData(data, time)

    if savingStatus:
        NotYetScanned = True
        response = process(data, time)
        return response
    else:
        return {"status":"data invalid"}

if __name__ == '__main__':
    app.run(debug=True, port=5000)

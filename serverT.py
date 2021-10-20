
import time
import threading
from wsgiref.simple_server import make_server
from flask import Flask, request
from process import process
from datetime import datetime

from utils import *




def get_app():
    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route("/processData", methods=["POST"])
    def processData():
        t = str(datetime.now())
        data=request.form.to_dict()
        savingStatus = saveData(data, t)

        if savingStatus:
            NotYetScanned = True
            response = process(data, t)
            return response
        else:
            return {"status":"data invalid"}
    return app


class WsgiRefServer(threading.Thread):

    def __init__(self, wsgi_app, host='', port=8080):
        super().__init__()

        self._server = make_server(host, port, wsgi_app)

    def run(self):
        self._server.serve_forever(poll_interval=0.5)

    def stop(self):

        self._server.shutdown()
        self.join()


if __name__ == '__main__':

    http_thread = WsgiRefServer(get_app())

    http_thread.start()

    time.sleep(60)
    http_thread.stop()


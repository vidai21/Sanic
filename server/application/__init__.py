import os
from .server import app

def run_app(host="127.0.0.1", port=8080, debug=False):
    app.run(host=host, port=port, debug=debug, workers=os.cpu_count())
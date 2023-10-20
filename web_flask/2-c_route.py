#!/usr/bin/python3
"""
Module - 2-c_route
Starts a Flask web application
    listening on 0.0.0.0, port 5000
"""
from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """
    Dislays Hello HBNB!
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb_route():
    """
    Dislays HBNB!
    """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """
    Dislays text in route
    """
    return f"C {text.replace('_', ' ')}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

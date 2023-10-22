#!/usr/bin/python3
"""
Module - 6-number_odd_or_even
Starts a Flask web application
    listening on 0.0.0.0, port 5000
"""
from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """
    Displays Hello HBNB!
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb_route():
    """
    Displays HBNB!
    """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """
    Displays “C ”, followed by the
    value of the text variable
    """
    return f"C {text.replace('_', ' ')}"


@app.route("/python/", defaults={'text': 'is_cool'}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text):
    """
    Displays “Python ”, followed by the
    value of the text variable
    """
    return f"Python {text.replace('_', ' ')}"


@app.route("/number/<int:n>", strict_slashes=False)
def number_route(n):
    """
    display “n is a number” only if n is an integer
    """
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """
     display a HTML page only if n is an integer
        H1 tag: “Number: n” inside the tag BODY
    """
    return render_template('5-number.html', n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    """
    display a HTML page only if n is an integer:
        H1 tag: “Number: n is even|odd” inside the tag BODY
    """
    odd_or_even = "even"
    if n % 2 != 0:
        odd_or_even = "odd"
    return render_template('6-number_odd_or_even.html', n=n,
                           odd_or_even=odd_or_even)


@app.teardown_appcontext
def tear_down(n):
    """
    Removes the current SQLAlchemy Session after
    each request
    """
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """
    Displays a HTML page: (inside the tag BODY)
        H1 tag: “States”
        UL tag: with the list of all State objects present in
        DBStorage sorted by name (A->Z) tip
        LI tag: description of one State: <state.id>: <B><state.name></B>
    """
    state_obj = [sts for sts in storage.all("State").values()]

    return render_template('7-states_list.html',
                           state_obj=state_obj)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

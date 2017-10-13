"""
Module for Flask API.
"""

from compute import Calculator

from flask import Flask, request, send_file

app = Flask(__name__)
calculator = Calculator()


@app.route('/graph')
def graph():
    """
    Returns the graph of the given expression
    """

    expression = request.args['exp']
    calculator.graph(expression, 'temp.png')

    return send_file('temp.png', mimetype='image/png')

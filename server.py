"""
Module for Flask API.
"""

from compute import Calculator
from flask import Flask, request, send_file     #pylint: disable=E0401

app = Flask(__name__)                           #pylint: disable=C0103
calculator = Calculator()                       #pylint: disable=C0103

@app.route('/solve')
def solve():
    """
    Returns the graph of the given expression
    """

    expression = request.args['exp']
    calculator.graph(expression, 'temp.png')

    return send_file('temp.png', mimetype='image/png')

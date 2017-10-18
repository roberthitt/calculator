"""
Module for Flask API.
"""

from flask import Flask, request, send_file

from . compute import Calculator

app = Flask(__name__)
calculator = Calculator('config.yaml')


@app.route('/graph')
def graph():
    """
    Returns the graph of the given expression
    """

    expression = request.args['exp']
    calculator.graph(expression, 'temp.png')

    return send_file('temp.png', mimetype='image/png')

"""
Module for Sanic API.
"""

from sanic import Sanic, response

from . compute import Calculator

app = Sanic()
calculator = Calculator('config.yaml')


@app.route('/graph')
async def graph(request):
    """
    Returns the graph of the given expression.
    """

    expression = request.args['exp'][0]
    print(expression)
    calculator.graph(expression, 'temp.png')

    return await response.file('temp.png')

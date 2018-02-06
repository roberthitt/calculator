"""
Module for Sanic API.
"""

import os
from math import isinf

from sanic import Sanic, response

from compute import Calculator
from extract import Extractor

app = Sanic()
calculator = Calculator('config.yaml')


@app.route('/valid')
async def check_valid(request):
    """
    Checks whether the given equation is valid.
    """

    expression = request.args['exp'][0]
    solution = calculator.solve(expression.replace('x', '(1)'))
    status = 'valid'

    if solution is None:
        status = 'unbalanced'
    elif isinf(solution):
        status = 'divByZero'

    return response.text(status)


@app.route('/graph')
async def graph(request):
    """
    Returns the graph of the given expression.
    """

    expression = request.args['exp'][0]
    calculator.graph(expression, 'temp.png')

    return await response.file('temp.png')


@app.route('/solve')
async def solve(request):
    """
    Returns the solution to the given expression.
    """

    expression = request.args['exp'][0]
    solution = calculator.solve(expression)

    return response.text(str(solution))


@app.route('/extract', methods=['POST'])
async def extract(request):
    """
    Returns the text contained in the image.
    """

    body = request.files['file'][0].body
    text = Extractor.extract(body)
    return response.text(text)

if __name__ == '__main__':
    port = os.environ.get('PORT') or 8080
    app.run(
        host='0.0.0.0',
        port=int(port),
        workers=4,
        debug=True
    )

"""
Module for Sanic API.
"""

import os
import datetime
from math import isinf

from sanic import Sanic, response
from sanic_cors import CORS

from compute import Calculator
from extract import Extractor

app = Sanic()
CORS(app)
calculator = Calculator('config.yaml')


@app.route('/valid')
async def check_valid(request):
    """
    Checks whether the given equation is valid.
    """

    expression = request.args.get('exp', '')
    replaced = expression.replace('x', '(1)')

    solution = calculator.solve(replaced)
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
    current_time = datetime.datetime.now().isoformat()
    image_path = f'images/{current_time}.png'

    expression = request.args.get('exp', '')
    calculator.graph(expression, image_path)

    return await response.file(image_path)


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

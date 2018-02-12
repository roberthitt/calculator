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
from storage import StorageEngine

app = Sanic()
CORS(app)
calculator = Calculator('config.yaml')
storage_engine = StorageEngine()


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
    # Save image based on time of creation.
    current_time = datetime.datetime.now()
    image_path = f'images/{current_time}.png'

    # Graph given expression.
    expression = request.args.get('exp', '')
    calculator.graph(expression, image_path)

    # Log graph info to database.
    storage_engine.add_image(current_time, image_path, expression)

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


@app.route('/history', methods=['GET'])
async def history(request):
    """
    Returns a log of all previous graphs.
    """

    log = storage_engine.get_image_history()

    return response.json(log)


@app.route('/image', methods=['GET'])
async def image(request):
    """
    Returns the graph stored at the given path.
    """
    path = request.args['path'][0]

    return await response.file(path)


if __name__ == '__main__':
    port = os.environ.get('PORT') or 8080
    app.run(
        host='0.0.0.0',
        port=int(port),
        workers=4,
        debug=True
    )


"""
Module for Sanic API.
"""

import os

from sanic import Sanic, response

from compute import Calculator

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

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=os.environ.get('PORT') or 8080,
        workers=4,
        debug=True
    )

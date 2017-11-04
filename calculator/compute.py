"""
Module for computing infix expressions and equations
"""

from collections import namedtuple, deque
from io import BytesIO
from tokenize import tokenize, NUMBER, ENCODING

from mpl_toolkits.axes_grid.axislines import SubplotZero
import matplotlib.pyplot as plt
import numpy as np

from . configuration import Configuration


class Calculator:
    """
    Class for computing infix expressions.

    Example:
    --------
    >>> computer = Calculator()
    >>> computer.solve('10+2 - (3*3)')
    3
    """

    OpInfo = namedtuple('Operator', 'precedence assoc operation operand_count')

    def __init__(self, config_path):
        config = Configuration(config_path)
        self.ops = config.ops

    def graph(self, equation, file_name=None, dimensions=(10, 10)):
        """
        Graphs a function of the form 'x + 5'.

        Args:
            equation: a string containing the right side of an equation
            file_name: name for plot to be serialized under.
            dimensions: a tuple of form (x, y).
                        domain will go from -x to x, and range from -y to y.
        """

        x_bounds, y_bounds = dimensions

        increments = np.linspace(-x_bounds, x_bounds, 10000)
        points = self.solve(equation, replacement=increments)

        # Filters out too large/small values.
        # Necessary for functions with discontinuous lines (e.g., tan).
        points[points > y_bounds] = np.nan
        points[points < -y_bounds] = np.nan

        self.create_plot(increments, points, y_bounds, file_name)

    def create_plot(self, scale, points, y_bounds, file_name=None):
        """
        Using matplotlib, graphs the given points on a Cartesian plane.

        Adapted from the matplotlib documentation:
        https://matplotlib.org/examples/axes_grid/demo_axisline_style.html.

        args:
            scale: Numpy array of increments for the x-axis.
            points: Numpy array of points' Y-values to be plotted.
            y_bounds: integer determining scale of y axis
            file_name: name for plot to be serialized under.
        """

        fig = plt.figure(1)
        subplot = SubplotZero(fig, 111)
        fig.add_subplot(subplot)

        for direction in ['xzero', 'yzero']:
            subplot.axis[direction].set_axisline_style('-|>')
            subplot.axis[direction].set_visible(True)

        for direction in ['left', 'right', 'bottom', 'top']:
            subplot.axis[direction].set_visible(False)

        subplot.set_ylim([-y_bounds, y_bounds])
        subplot.plot(scale, points)

        if file_name:
            plt.savefig(file_name)
        else:
            plt.show()

        g = Graph('cs-321-project','BTAPeQhBPbR6SkKQDkkU')
	g.create_graph('graph_name','graph_title', data)


    def solve(self, expression, replacement=None):
        """
        Solves an infix algebraic expression.

        Adapted from the pseudocode shown here:
        https://en.wikipedia.org/wiki/Reverse_Polish_notation#Postfix_evaluation_algorithm.

        Args:
            expression: string containing an expression in infix notation
            replacement: optional Numpy array to replace the variable 'x'

        Returns:
            float result of the expression
        """

        if replacement is not None:
            # Necessary for supporting expressions like 5x.
            expression = expression.replace('x', '(x)')

        postfix_queue = self.convert_infix(expression)
        eval_stack = []

        try:
            for token in postfix_queue:
                if token == 'x':
                    eval_stack.append(replacement)
                elif token in self.ops:
                    *_, operation, operand_count = self.ops[token]

                    # Pops a variable number of items off the stack.
                    operands = eval_stack[-operand_count:]
                    eval_stack = eval_stack[:-operand_count]

                    result = operation(*operands)
                    eval_stack.append(result)
                else:
                    eval_stack.append(token)

            return eval_stack.pop()
        except ValueError:
            return None

    def convert_infix(self, expression):
        """
        Converts an infix expression to a postfix expression
        Uses a modified version of the Shunting-Yard algorithm.

        Adapted from the pseudocode shown here:
        https://en.wikipedia.org/wiki/Shunting-yard_algorithm.

        Args:
            expression: a string containing an expression in infix notation

        Returns:
            queue of tuples containing operands and operators in postfix order
        """

        # Breaks the expression string into a list of tokens
        tokens = list(tokenize(BytesIO(expression.encode('utf_8')).readline))

        out_queue = deque()
        op_stack = []
        prev_token = (None, None)

        for tok_type, tok_string, *_ in tokens:
            prev_tok_type, prev_tok_string = prev_token

            if tok_type == NUMBER:
                out_queue.append(float(tok_string))
            elif tok_string == 'x':
                out_queue.append(tok_string)
            elif tok_string == '(':
                # Allow implicit multiplication (e.g., c(x) or (x)(y)).
                if (prev_tok_type == NUMBER or
                        prev_tok_string == 'x' or prev_tok_string == ')'):
                    op_stack.append('*')

                op_stack.append(tok_string)

            elif tok_string == ')':
                while op_stack and op_stack[-1] != '(':
                    out_queue.append(op_stack.pop())
                op_stack.pop()

            elif tok_string in self.ops:
                # Allow unary minus operator.
                if (tok_string == '-' and prev_tok_string != ')' and
                        (prev_tok_string == 'x' or
                         prev_tok_string in self.ops or
                         prev_tok_string == '(' or
                         prev_tok_string is None)):

                    tok_string = 'neg'
                while op_stack:
                    top = op_stack[-1]
                    if top == '(':
                        break

                    top_info = self.ops[top]
                    current_info = self.ops[tok_string]
                    if (top_info.assoc == 'L' and
                            top_info.precedence >= current_info.precedence):
                        out_queue.append(op_stack.pop())
                    else:
                        break
                op_stack.append(tok_string)

            if tok_type != ENCODING:
                prev_token = (tok_type, tok_string)

        while op_stack:
            out_queue.append(op_stack.pop())

        return out_queue

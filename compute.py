"""
Module for computing infix expressions and equations
"""

import operator
import math
from collections import namedtuple, deque
from io import BytesIO
from tokenize import tokenize, NUMBER, ENCODING

from mpl_toolkits.axes_grid.axislines import SubplotZero
import matplotlib.pyplot as plt
import numpy as np


class Calculator:
    """
    Class for computing infix expressions.

    >>> computer = Calculator()
    >>> computer.solve('10+2 - (3*3)')
    3
    """

    OpInfo = namedtuple('Operator', 'precedence assoc operation operand_count')

    def __init__(self):
        ## TODO: consider moving this to a seperate config file
        self.OPS = {
            'neg': self.OpInfo(precedence=5, assoc='R', operation=operator.neg, operand_count=1),
            'abs': self.OpInfo(precedence=4, assoc='L', operation=operator.abs, operand_count=1),
            'sin': self.OpInfo(precedence=4, assoc='L', operation=math.sin, operand_count=1),
            'cos': self.OpInfo(precedence=4, assoc='L', operation=math.cos, operand_count=1),
            'tan': self.OpInfo(precedence=4, assoc='L', operation=math.tan, operand_count=1),
            'sqrt': self.OpInfo(precedence=4, assoc='L', operation=math.sqrt, operand_count=1),
            'log': self.OpInfo(precedence=4, assoc='L', operation=math.log10, operand_count=1),
            'ln': self.OpInfo(precedence=4, assoc='L', operation=math.log, operand_count=1),
            '!': self.OpInfo(precedence=4, assoc='R', operation=math.factorial, operand_count=1),
            '^': self.OpInfo(precedence=3, assoc='R', operation=operator.pow, operand_count=2),
            '*': self.OpInfo(precedence=2, assoc='L', operation=operator.mul, operand_count=2),
            '/': self.OpInfo(precedence=2, assoc='L', operation=operator.truediv, operand_count=2),
            '+': self.OpInfo(precedence=1, assoc='L', operation=operator.add, operand_count=2),
            '-': self.OpInfo(precedence=1, assoc='L', operation=operator.sub, operand_count=2)
        }

    def graph(self, equation, dimensions=(10, 10)):
        """
        Graphs a function of the form 'y = x + 5'.

        Args:
            equation: a string containing the right side of an equation (the left side is implied)
            dimensions: a tuple of the form (x, y). domain will go from -x to x, and range from -y to y
        """

        # Note: if performance is an issue, consider rewriting to use np operators
        #       to operate on the entire np array rather than individual elements

        x, y = dimensions

        increments = np.linspace(-x, x, 1000)
        points = np.fromiter((self.solve(equation, replacement=value) for value in increments), np.float)

        # Necessary for functions with discontinuous lines.
        points[points > y] = np.nan
        points[points < -y] = np.nan

        self.create_plot(increments, points, y)

    def create_plot(self, scale, points, y_bounds):
        """
        Using matplotlib, graphs the given points on a Cartesian plane.

        Adapted from the matplotlib documentation:
        https://matplotlib.org/examples/axes_grid/demo_axisline_style.html.

        args:
            scale: Numpy array of increments for the x-axis.
            points: Numpy array of points' Y-values to be plotted.
            y_bounds: integer determining scale of y axis. range will go from -y_bounds to y_bounds.
        """

        fig = plt.figure(1)
        ax = SubplotZero(fig, 111)
        fig.add_subplot(ax)

        for direction in ['xzero', 'yzero']:
            ax.axis[direction].set_axisline_style('-|>')
            ax.axis[direction].set_visible(True)

        for direction in ['left', 'right', 'bottom', 'top']:
            ax.axis[direction].set_visible(False)

        ax.set_ylim([-y_bounds, y_bounds])
        ax.plot(scale, points)

        plt.show()

    def solve(self, expression, replacement=None):
        """
        Solves an infix algebraic expression.

        Adapted from the pseudocode shown here:
        https://en.wikipedia.org/wiki/Reverse_Polish_notation#Postfix_evaluation_algorithm.

        Args:
            expression: a string containing an algebraic expression in infix notation
            replacement: optional value to replace the variable 'x' if it occurs in expression

        Returns:
            integer or float result of the expression
        """

        if replacement is not None:
            expression = expression.replace('x', f'({replacement})')

        postfix_queue = self.convert_infix(expression)
        eval_stack = []

        try:
            for token in postfix_queue:
                if token in self.OPS:
                    *_, operation, operand_count = self.OPS[token]

                    # Pops a variable number of items off the stack.
                    operands = eval_stack[-operand_count:]
                    eval_stack = eval_stack[:-operand_count]

                    #print(f'{token} {operands}')
                    result = operation(*operands)
                    eval_stack.append(result)
                else:
                    eval_stack.append(token)

            return eval_stack.pop()
        except ValueError:
            return None


    def convert_infix(self, expression):
        """
        Converts an infix expression to a postfix expression using the Shunting-Yard algorithm.

        Adapted from the pseudocode shown here:
        https://en.wikipedia.org/wiki/Shunting-yard_algorithm.

        Args:
            expression: a string containing an algebraic expression in infix notation

        Returns:
            a queue of tuples containing operands and operators in postfix order
        """

        # Breaks the expression string into a list of tokens, expressed as 5-tuples.
        tokens = list(tokenize(BytesIO(expression.encode('utf_8')).readline))

        out_queue = deque()
        op_stack = []
        prev_token = (None, None)

        for tok_type, tok_string, *_ in tokens:
            prev_tok_type, prev_tok_string = prev_token

            if tok_type == NUMBER:
                out_queue.append(float(tok_string))

            elif tok_string == '(':
                # Allow implicit multiplication (eg 5(x) or (x)(y))
                if prev_tok_type == NUMBER or prev_tok_string == ')':
                    op_stack.append('*')

                op_stack.append(tok_string)

            elif tok_string == ')':
                while op_stack and op_stack[-1] != '(':
                    out_queue.append(op_stack.pop())
                op_stack.pop()

            elif tok_string in self.OPS:
                # Allow unary minus operator
                if tok_string == '-' and (prev_tok_string in self.OPS or prev_tok_string == '('
                    or prev_tok_string == None) and prev_tok_string != ')':

                    tok_string = 'neg'

                while op_stack:
                    top = op_stack[-1]
                    if top == '(':
                        break

                    top_info, current_info = self.OPS[top], self.OPS[tok_string]
                    if top_info.assoc == 'L' and top_info.precedence >= current_info.precedence:
                        out_queue.append(op_stack.pop())
                    else:
                        break
                op_stack.append(tok_string)

            if tok_type != ENCODING:
                prev_token = (tok_type, tok_string)

        while op_stack:
            out_queue.append(op_stack.pop())

        return out_queue

com = Calculator()
com.graph('sqrt(x) + 5')
com.graph('log(x) + 5')
com.graph('ln(x) + 5')

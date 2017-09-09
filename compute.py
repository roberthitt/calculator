"""
Module for computing infix expressions and equations
"""

from collections import namedtuple, deque
from io import BytesIO
from tokenize import tokenize, NUMBER, OP

import operator


OpInfo = namedtuple('Operator', 'precedence assoc operation')

class ExpressionComputer:
    """
    Class for computing infix expressions.

    >>> computer = ExpressionComputer()
    >>> computer.solve('10+2 - (3*3)')
    3
    """


    def __init__(self):
        self.ops = {
            '^': OpInfo(precedence=3, assoc='R', operation=operator.pow),
            '*': OpInfo(precedence=2, assoc='L', operation=operator.mul),
            '/': OpInfo(precedence=2, assoc='L', operation=operator.truediv),
            '+': OpInfo(precedence=1, assoc='L', operation=operator.add),
            '-': OpInfo(precedence=1, assoc='L', operation=operator.sub)
        }

    def solve(self, expression):
        """
        Solves an infix algebraic expression.

        Args:
            expression: a string containing an algebraic expression in infix notation

        Returns:
            integer or float result of the expression
        """

        postfix_queue = self.convert_infix(expression)
        eval_stack = []

        for tok_type, token in postfix_queue:
            if tok_type == OP:
                operand2, operand1 = eval_stack.pop(), eval_stack.pop()
                result = self.ops[token].operation(operand1, operand2)
                eval_stack.append(result)
            else:
                eval_stack.append(token)

        return eval_stack.pop()

    def convert_infix(self, expression):
        """
        Converts an infix expression to a postfix expression using the Shunting-Yard algorithm.

        Args:
            expression: a string containing an algebraic expression in infix notation

        Returns:
            a queue of tuples containing operands and operators in postfix order
        """

        # Breaks the expression string into a list of tokens, expressed as 5-tuples.
        tokens = list(tokenize(BytesIO(expression.encode('utf_8')).readline))

        out_queue = deque()
        op_stack = []
        for tok_type, tok_string, *_ in tokens:
            if tok_type == NUMBER:
                out_queue.append((tok_type, int(tok_string)))
            elif tok_string == '(':
                op_stack.append((tok_type, tok_string))
            elif tok_string == ')':
                while op_stack and op_stack[-1][1] != '(':
                    out_queue.append(op_stack.pop())
                op_stack.pop()
            elif tok_type == OP:
                while op_stack:
                    top = op_stack[-1][1]
                    if top == '(':
                        break

                    top_info, current_info = self.ops[top], self.ops[tok_string]
                    if top_info.assoc == 'L' and top_info.precedence >= current_info.precedence:
                        out_queue.append(op_stack.pop())
                    else:
                        break
                op_stack.append((tok_type, tok_string))

        while op_stack:
            out_queue.append(op_stack.pop())

        return out_queue

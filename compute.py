"""
Module for computing infix expressions and equations
"""

from collections import namedtuple, deque
from io import BytesIO
from tokenize import tokenize, NUMBER, OP


class ExpressionComputer:
    """
    Class for computing infix expressions

    >>> computer = ExpressionComputer()
    >>> computer.solve('10+2 - (3*3)')
    "3"
    """

    def __init__(self):
        Operator = namedtuple('Operator', 'prec assoc')
        self.ops = {
            '^': Operator(prec=3, assoc='R'),
            '*': Operator(prec=2, assoc='L'),
            '/': Operator(prec=2, assoc='L'),
            '+': Operator(prec=1, assoc='L'),
            '-': Operator(prec=1, assoc='L')
        }

    def solve(self, expression):
        # Breaks the expression string into a list of tokens, expressed as 5-tuples.
        tokens = list(tokenize(BytesIO(expression.encode('utf_8')).readline))

        print('Before:')
        print(expression)
        postfix_queue = self.convert_infix(tokens)
        print('After:')
        print(*[x[1] for x in postfix_queue])

    def convert_infix(self, tokens):
        """
        Converts an infix expression to a postfix expression using the Shunting-Yard algorithm.

        Args:
            tokens: a list of tuples containing operators and operands in infix order

        Returns:
            a queue of tuples containing operands and operators in postfix order
        """

        out_queue = deque()
        op_stack = []
        for tok_type, tok_string, *_ in tokens:
            if tok_type == NUMBER:
                out_queue.append((tok_type, tok_string))
            elif tok_string == '(':
                op_stack.append((tok_type, tok_string))
            elif tok_string == ')':
                while op_stack and op_stack[-1][1] != '(':
                    out_queue.append(op_stack.pop())
                op_stack.pop()
            elif tok_type == OP:
                while op_stack:
                    operator = op_stack[-1][1]
                    if operator == '(':
                        break

                    op_info, tok_info = self.ops[operator], self.ops[tok_string]
                    if op_info.assoc == 'L' and op_info.prec >= tok_info.prec:
                        out_queue.append(op_stack.pop())
                    else:
                        break
                op_stack.append((tok_type, tok_string))

        while op_stack:
            out_queue.append(op_stack.pop())

        return out_queue


com = ExpressionComputer()
com.solve('3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3')

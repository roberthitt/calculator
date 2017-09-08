"""
Module for computing infix expressions and equations
"""

from collections import namedtuple
from io import BytesIO
from tokenize import tokenize, NUMBER, OP


class ExpressionComputer:
    """
    Class for computing infix expressions

    >>> computer = ExpressionComputer('10+2 - (3*3)')
    >>> computer.solve()
    "3"
    """

    def __init__(self, expression):
        Operator = namedtuple('Operator', 'prec assoc')
        self.ops = {
            '^': Operator(prec=3, assoc='R'),
            '*': Operator(prec=2, assoc='L'),
            '/': Operator(prec=2, assoc='L'),
            '+': Operator(prec=1, assoc='L'),
            '-': Operator(prec=1, assoc='L')
        }
        self.expression = expression

        # Breaks the expression string into a list of tokens, expressed as 5-tuples.
        # The tuples are of the form (token type, token string, (srow, scol), (erow, ecol), line).
        self.tokens = tokenize(BytesIO(expression.encode('utf_8')).readline)

    def solve(self):
        print('Before:')
        print(self.expression)
        postfix_stack = self.convert_infix()
        print('After:')
        print(*[x[1] for x in postfix_stack])

    def convert_infix(self):
        """
        Converts an infix expression to a postfix expression using the Shunting-Yard algorithm.

        Returns:
            a stack containing the operands and operators in postfix form
        """

        out_stack = []
        op_stack = []
        for tok_type, tok_string, *_ in list(self.tokens):
            if tok_type == NUMBER:
                out_stack.append((tok_type, tok_string))
            elif tok_string == '(':
                op_stack.append((tok_type, tok_string))
            elif tok_string == ')':
                while op_stack and op_stack[-1][1] != '(':
                    out_stack.append(op_stack.pop())
                op_stack.pop()
            elif tok_type == OP:
                while op_stack:
                    operator = op_stack[-1][1]
                    if operator == '(':
                        break

                    op_info, tok_info = self.ops[operator], self.ops[tok_string]
                    if op_info.assoc == 'L' and op_info.prec >= tok_info.prec:
                        out_stack.append(op_stack.pop())
                    else:
                        break
                op_stack.append((tok_type, tok_string))

        while op_stack:
            out_stack.append(op_stack.pop())

        return out_stack


com = ExpressionComputer('3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3')
com.solve()

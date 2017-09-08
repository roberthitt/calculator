"""
Module for computing infix expressions and equations
"""

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
        self.expression = expression

    def solve(self):
        print('Before:')
        print(self.expression)
        postfix_stack = self.convert_infix(self.expression)
        print('After:')
        print(*[x[1] for x in postfix_stack])


    def convert_infix(self, expression):
        """
        Converts an infix expression to a postfix expression using the Shunting-Yard algorithm.

        Args:
            expression: string containing the infix expression

        Returns:
            a stack containing the operands and operators in postfix form
        """

        # Precedence rules for operators
        precedence = {'^': 5, '*': 4, '/': 3, '+': 2, '-': 1}
        right_assoc = ['^']

        out_stack = []
        op_stack = []

        # Breaks the expression string into a list of tokens, expressed as 5-tuples.
        # The tuples are of the form (token type, token string, (srow, scol), (erow, ecol), line).
        tokens = list(tokenize(BytesIO(expression.encode('utf_8')).readline))

        for tok_type, tok_string, *_ in tokens:
            if tok_type == NUMBER:
                out_stack.append((tok_type, tok_string))
            elif tok_string == '(':
                op_stack.append((tok_type, tok_string))
            elif tok_string == ')':
                while op_stack and op_stack[-1][1] != '(':
                    out_stack.append(op_stack.pop())
                op_stack.pop()
            elif tok_type == OP:
                while (op_stack and op_stack[-1][1] != '('
                       and op_stack[-1][1] not in right_assoc
                       and precedence[op_stack[-1][1]] >= precedence[tok_string]):
                    out_stack.append(op_stack.pop())
                op_stack.append((tok_type, tok_string))

        while op_stack:
            out_stack.append(op_stack.pop())

        return out_stack


com = ExpressionComputer('3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3')
com.solve()

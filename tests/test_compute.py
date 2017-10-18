"""
Module for testing the compute.py module
"""

import pytest


@pytest.fixture(scope="module")
def calc():
    from .. calculator.compute import Calculator
    return Calculator('config.yaml')


def test_solve_add(calc):
    assert calc.solve('5+5') == 10


def test_solve_mult(calc):
    assert calc.solve('5*5') == 25


def test_solve_exp(calc):
    assert calc.solve('5^2') == 25


def test_solve_parens(calc):
    assert calc.solve('2*(5+5)') == 20


def test_solve_precedence(calc):
    assert calc.solve('2 + 5 * 5') == 27


def test_solve_trig(calc):
    assert calc.solve('sin(1)') == 0.8414709848078965


def test_solve_unary_minus(calc):
    assert calc.solve('-5') == -5
    assert calc.solve('-(2 + 3)') == -5


def test_solve_unbalanced(calc):
    with pytest.raises(Exception) as excinfo:
        calc.solve('(5+')
    assert str(excinfo.value) == 'Input contains unbalanced parentheses'

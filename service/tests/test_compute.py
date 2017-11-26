"""
Module for testing the compute.py module
"""

import pytest


@pytest.fixture(scope="module")
def calc():
    from .. compute import Calculator
    return Calculator('config.yaml')


def test_solve_add(calc):
    assert calc.solve('5+5') == 10
    assert calc.solve('5+(-5)') == 0
    assert calc.solve('-6+6') == 0
    assert calc.solve('-5+0') == -5
    assert calc.solve('0+6') == 6
    assert calc.solve('0-(-8)') == 8

def test_solve_mult(calc):
    assert calc.solve('5*5') == 25
    assert calc.solve('-6*6') == -36
    assert calc.solve('-2*-3') == 6
    assert calc.solve('100*-2') == -200
    assert calc.solve('10*0') == 0
    assert calc.solve('0*0') == 0

def test_solve_exp(calc):
    assert calc.solve('5^2') == 25
    assert calc.solve('8^-2') == 0.015625
    assert calc.solve('10^-5') == 0.00001
    assert calc.solve('-10^2') == -100
    assert calc.solve('-4^-2') == -0.0625
    assert calc.solve('7^8') == 5764801

def test_solve_parens(calc):
    assert calc.solve('2*(5+5)') == 20
    assert calc.solve('(2+2)-(8-4)') == 0
    assert calc.solve('3^(-2+2)') == 1
    assert calc.solve('((5+4)^2) + 1') == 82


def test_solve_precedence(calc):
    assert calc.solve('2 + 5 * 5') == 27
    assert calc.solve('(2+5)*5') == 35
    assert calc.solve('8 * (2*5)') == 80
    assert calc.solve('8 * 2 / 5') == 3.2


def test_solve_trig(calc):
    assert calc.solve('sin(1)') == 0.8414709848078965
    assert calc.solve('cos(1)') == 0.54030230586
    assert calc.solve('cos(0)') == 1
    assert calc.solve('sin(0)') == 0
    assert calc.solve('tan(1)') == 1.55740772465
    assert calc.solve('tan(0)') == 0

def test_solve_trigadd(calc):
    assert calc.solve('sin(0) + cos(1)') == 0.54030230586
    assert calc.solve('cos(2) + sin(2)') == 0.49315059027
    assert calc.solve('cos(0) + 20') == 20
    assert calc.solve('sin(0) + cos(0)') == 1
    assert calc.solve('sin(0) + tan(0)') == 0

def test_solve_unary_minus(calc):
    assert calc.solve('-5') == -5
    assert calc.solve('-(2 + 3)') == -5
    assert calc.solve('5-(-5)') == 10
    assert calc.solve('-4-4') == -8
    assert calc.solve('-8+8') == 0
    assert calc.solve('5 - 0') == 5
    assert calc.solve('0-0') == 0


def test_solve_unbalanced(calc):
    with pytest.raises(Exception) as excinfo:
        calc.solve('(5+')
    assert str(excinfo.value) == 'Input contains unbalanced parentheses'

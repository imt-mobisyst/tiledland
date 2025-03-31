import sys, hacka.py as hacka

"""
Test - Pick'n Del Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.tiledland.game.pickndel as pnd
import src.tiledland as tll


def test_pnd_initCarrier():
    carrier= pnd.Carrier()
    assert str(carrier) == "Carrier-1.0 ⌊(-0.18, -0.18), (0.18, 0.18)⌉ |0, 0|"

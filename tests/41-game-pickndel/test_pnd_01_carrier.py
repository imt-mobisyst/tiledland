import sys, hacka, tiledland as tild

"""
Test - Pick'n Del Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.tiledland.game.pickndel as pnd

"""
Test - Carrier
"""

def test_pnd_fast_initCarrier():
    carrier= pnd.Carrier()
    assert str(carrier) == "0:Car 0-0 ⌊(-0.26, -0.3), (0.3, 0.3)⌉ |0, 0|"

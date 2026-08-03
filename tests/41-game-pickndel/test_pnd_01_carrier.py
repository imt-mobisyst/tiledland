import sys, hacka, tiledland as tll

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
    assert str(carrier) == "Carrier |0, 0|"

import sys, hacka as hacka

"""
Test - Coffee Fleet Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.tiledland as tll
import src.tiledland.game.coffeefleet as cfg

def test_pnd_initCarrier():
    bot= cfg.Bot()
    assert type(bot) == cfg.Bot
    # assert str(carrier) == "Carrier-1.0 ⌊(-0.18, -0.18), (0.18, 0.18)⌉ |0, 0|"

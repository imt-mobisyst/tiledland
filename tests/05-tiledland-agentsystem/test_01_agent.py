# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland.geometry import Convex, Point

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_fast_agent_init():
    agent= tll.Agent()
    assert type(agent) == tll.Agent

    assert agent.stateInfinitWait.__self__ == agent
    assert agent.stateInfinitWait.__func__ == tll.Agent.stateInfinitWait

    assert agent._statePs == tll.Agent.stateInitialize

    a= agent.runStateProcessus()
    assert a.identifier() == tll.Action.WAIT
    assert a.attributes() == []
    assert agent._statePs == tll.Agent.stateInfinitWait

    a= agent.runStateProcessus()
    assert a.identifier() == tll.Action.WAIT
    assert a.attributes() == []
    assert agent._statePs == tll.Agent.stateInfinitWait

def test_fast_agent_copy():
    model= tll.Agent()
    agent= model.copy()
    
    assert agent._statePs ==  tll.Agent.stateInitialize
    
    a= agent.runStateProcessus()
    assert a.identifier() == tll.Action.WAIT
    assert a.attributes() == []

    assert agent._statePs == tll.Agent.stateInfinitWait
    assert model._statePs ==  tll.Agent.stateInitialize
    
    model= agent.copy()

    assert model._statePs ==  tll.Agent.stateInfinitWait

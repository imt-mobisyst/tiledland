# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tild
from src.tiledland.geometry import Convex, Point

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_fast_agent_init():
    agent= tild.Agent()
    assert type(agent) == tild.Agent

    assert agent.stateInfinitWait.__self__ == agent
    assert agent.stateInfinitWait.__func__ == tild.Agent.stateInfinitWait

    assert agent._statePs == tild.Agent.stateInitialize

    a= agent.runStateProcessus()
    assert a.identifier() == tild.Action.WAIT
    assert a.attributes() == []
    assert agent._statePs == tild.Agent.stateInfinitWait

    a= agent.runStateProcessus()
    assert a.identifier() == tild.Action.WAIT
    assert a.attributes() == []
    assert agent._statePs == tild.Agent.stateInfinitWait

def test_fast_agent_copy():
    model= tild.Agent()
    agent= model.copy()
    
    assert agent._statePs ==  tild.Agent.stateInitialize
    
    a= agent.runStateProcessus()
    assert a.identifier() == tild.Action.WAIT
    assert a.attributes() == []

    assert agent._statePs == tild.Agent.stateInfinitWait
    assert model._statePs ==  tild.Agent.stateInitialize
    
    model= agent.copy()

    assert model._statePs ==  tild.Agent.stateInfinitWait

# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland import Agent, Shape, Float2

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_Agent_init():
    agent= Agent()

    assert type(agent) == Agent
    assert agent.name() == "A"
    print( f"{agent.position()} == {Float2(0.0, 0.0)}") 

    assert agent.position() == Float2(0.0, 0.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in agent.envelope() ]
    assert env == [(-0.23, 0.1), (-0.1, 0.23), (0.1, 0.23), (0.23, 0.1), (0.23, -0.1), (0.1, -0.23), (-0.1, -0.23), (-0.23, -0.1)]

    agent.position().set(1.0, 2.0)
    assert agent.position() == Float2(1.0, 2.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in agent.envelope() ]
    assert env == [(0.77, 2.1), (0.9, 2.23), (1.1, 2.23), (1.23, 2.1), (1.23, 1.9), (1.1, 1.77), (0.9, 1.77), (0.77, 1.9)]

def test_Agent_init2():
    agent= Agent( "Bob", Float2(1.0, 2.0) )

    assert agent.name() == "Bob"
    assert agent.position() == Float2(1.0, 2.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in agent.envelope() ]
    assert env == [(0.77, 2.1), (0.9, 2.23), (1.1, 2.23), (1.23, 2.1), (1.23, 1.9), (1.1, 1.77), (0.9, 1.77), (0.77, 1.9)]
    
def test_Agent_str():
    agent= Agent( "Bob", Float2(1.0, 2.0) )
    assert str(agent) == "Bob on (1.0, 2.0)"

def test_Agent_podable():
    agent= Agent( "Bob", Float2(1.0, 2.0) )

    assert agent.wordAttributes() == ["Agent", "Bob"]
    assert agent.intAttributes() == []
    assert agent.floatAttributes() == [1.0, 2.0]
    assert agent.children() == [ agent.body() ]

def test_Agent_podable():
    agent= Agent( "Bob", Float2(1.0, 2.0) )

    assert agent.wordAttributes() == ["Agent", "Bob"]
    assert agent.intAttributes() == []
    assert agent.floatAttributes() == [1.0, 2.0]
    assert agent.children() == [ agent.body() ]

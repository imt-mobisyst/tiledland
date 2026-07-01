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
    assert agent.id() == 0
    print( f"{agent.position()} == {Point(0.0, 0.0)}") 

    assert agent.position() == Point(0.0, 0.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in agent.body().asZipped() ]
    
    print( env ) 
    assert env == [(-0.43, -0.25), (-0.43, 0.25), (0.0, 0.5), (0.5, 0.0), (0.0, -0.5)]

    agent.setShape( Convex().initRegular(0.5, 8) )
    env= [ ( round(x, 2), round(y, 2) ) for x, y in agent.body().asZipped() ]
    print( env )
    assert env == [(-0.23, -0.1), (-0.23, 0.1), (-0.1, 0.23), (0.1, 0.23), (0.23, 0.1), (0.23, -0.1), (0.1, -0.23), (-0.1, -0.23)]

    agent.setPosition(1.0, 2.0)
    assert agent.position() == Point(1.0, 2.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in agent.body().asZipped() ]
    print( env )
    assert env == [(0.77, 1.9), (0.77, 2.1), (0.9, 2.23), (1.1, 2.23), (1.23, 2.1), (1.23, 1.9), (1.1, 1.77), (0.9, 1.77)]

def test_fast_agent_init2():
    agent= tll.Agent( 42, 0, Convex().initRegular(0.5, 8) )
    agent.setPosition(1.0, 2.0)

    assert agent.id() == 42
    assert agent.position() == Point(1.0, 2.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in agent.body().asZipped() ]
    print( env )
    assert env == [(0.77, 1.9), (0.77, 2.1), (0.9, 2.23), (1.1, 2.23), (1.23, 2.1), (1.23, 1.9), (1.1, 1.77), (0.9, 1.77)]
    
def test_fast_agent_body():
    pos= Point(1.0, 2.0)
    agent= tll.Agent( 42, 0, Convex().initSquare(1.0) )
    agent.setPosition(pos.x(), pos.y())

    ref= [ Point(-0.5, -0.5), Point(-0.5, 0.5), Point(0.5, 0.5), Point(0.5, -0.5)]
    assert agent.referenceShape().asZipped() == [ p.asTuple() for p in ref ]
    assert agent.body().asZipped() == [ (p+pos).asTuple() for p in ref ]

    agent= tll.Agent( 42, 1, Convex().initSquare(1.0) )
    agent.setPosition(1.0, 2.0)
    print(agent)
    assert str(agent) == "Agent-1.42 ⌊(0.5, 1.5), (1.5, 2.5)⌉"


def test_fast_agent_str():
    agent= tll.Agent( 42, 0, Convex().initSquare(1.0), Point(1.0, 2.0) )
    print(agent)
    assert str(agent) == "Agent-42 ⌊(0.5, 1.5), (1.5, 2.5)⌉"

    agent= tll.Agent( 42, 1, Convex().initSquare(1.0) )
    agent.setPosition(1.0, 2.0)
    print(agent)
    assert str(agent) == "Agent-1.42 ⌊(0.5, 1.5), (1.5, 2.5)⌉"

def test_fast_agent_hacka():
    agent= tll.Agent( 42, 4 ).setPose( Point(1.0, 2.0), 1.5 )
    tree= agent.asDataTree()

    assert tree.label() == "Agent"
    assert tree.numberOfDigits() == 3
    assert tree.digits() == [42, 4, 0]
    assert tree.digit(1) == 42
    assert tree.digit(2) == 4
    assert tree.digit(3) == 0
    assert tree.numberOfValues() == 3
    assert tree.values() == [1.0, 2.0, 1.5]
    assert tree.value(1) == 1.0
    assert tree.value(2) == 2.0
    assert tree.numberOfChildren() == 1
    assert tree.children() == [ agent.referenceShape().asDataTree() ]

    agent2= tll.Agent().fromDataTree(tree)
    tree2= agent2.asDataTree()

    print(tree)
    print("vs")
    print(tree2)
    
    assert str(tree2) == str(tree)

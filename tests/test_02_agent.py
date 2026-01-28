# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland.geometry import Convex, Point

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_Agent_init():
    agent= tll.Agent()

    assert type(agent) == tll.Agent
    assert agent.id() == 0
    print( f"{agent.position()} == {Point(0.0, 0.0)}") 

    assert agent.position() == Point(0.0, 0.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in agent.body().asZipped() ]
    assert env == [(-0.2, -0.2), (-0.2, 0.2), (0.2, 0.2), (0.2, -0.2)]

    agent.setShape( Convex().initializeRegular(0.5, 8) )
    env= [ ( round(x, 2), round(y, 2) ) for x, y in agent.body().asZipped() ]
    print( env )
    assert env == [(-0.23, -0.1), (-0.23, 0.1), (0.1, 0.23), (0.23, 0.1), (0.23, -0.1), (0.1, -0.23), (-0.1, -0.23)]

    env= [ ( round(x, 2), round(y, 2) ) for x, y in agent.body().asZipped() ]
    print( env )
    assert env == [(-0.23, -0.1), (-0.23, 0.1), (0.1, 0.23), (0.23, 0.1), (0.23, -0.1), (0.1, -0.23), (-0.1, -0.23)]

    agent.position().set(1.0, 2.0)
    assert agent.position() == Point(1.0, 2.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in agent.body().asZipped() ]
    print( env )
    assert env == [(0.77, 1.9), (0.77, 2.1), (1.1, 2.23), (1.23, 2.1), (1.23, 1.9), (1.1, 1.77), (0.9, 1.77)]

def test_Agent_init2():
    agent= tll.Agent( 42, 0, Point(1.0, 2.0), Convex().initializeRegular(0.5, 8) )
    
    assert agent.id() == 42
    assert agent.position() == Point(1.0, 2.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in agent.body().asZipped() ]
    print( env )
    assert env == [(0.77, 1.9), (0.77, 2.1), (1.1, 2.23), (1.23, 2.1), (1.23, 1.9), (1.1, 1.77), (0.9, 1.77)]
    
def test_Agent_body():
    pos= Point(1.0, 2.0)
    agent= tll.Agent( 42, 0, pos, Convex().initializeSquare(1.0) )

    ref= [ Point(-0.5, -0.5), Point(-0.5, 0.5), Point(0.5, 0.5), Point(0.5, -0.5)]
    assert agent.shape().asZipped() == [ p.asTuple() for p in ref ]
    assert agent.body().asZipped() == [ (p+pos).asTuple() for p in ref ]

    agent= tll.Agent( 42, 1, Point(1.0, 2.0), Convex().initializeSquare(1.0) )
    print(agent)
    assert str(agent) == "Agent-1.42 ⌊(0.5, 1.5), (1.5, 2.5)⌉"


def test_Agent_str():
    agent= tll.Agent( 42, 0, Point(1.0, 2.0), Convex().initializeSquare(1.0) )
    print(agent)
    assert str(agent) == "Agent-42 ⌊(0.5, 1.5), (1.5, 2.5)⌉"

    agent= tll.Agent( 42, 1, Point(1.0, 2.0), Convex().initializeSquare(1.0) )
    print(agent)
    assert str(agent) == "Agent-1.42 ⌊(0.5, 1.5), (1.5, 2.5)⌉"

def test_Agent_podable():
    agent= tll.Agent( 42, 4, Point(1.0, 2.0) )
    pod= agent.asPod()

    assert pod.numberOfWords() == 1
    assert pod.words() == ["Agent"]
    assert pod.word() == "Agent"
    assert pod.numberOfIntegers() == 4
    assert pod.integers() == [42, 4, 14, 0]
    assert pod.integer(1) == 42
    assert pod.integer(2) == 4
    assert pod.integer(3) == 14
    assert pod.integer(4) == 0
    assert pod.numberOfValues() == 2
    assert pod.values() == [1.0, 2.0]
    assert pod.value(1) == 1.0
    assert pod.value(2) == 2.0
    assert pod.numberOfChildren() == 1
    assert pod.children() == [ agent.shape().asPod() ]

    agent2= tll.Agent().fromPod(pod)
    pod2= agent2.asPod()

    assert str(pod2) == str(pod)

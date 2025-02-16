# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland import Body, Shape, Float2

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_Body_init():
    body= Body()

    assert type(body) == Body
    assert body.id() == 0
    print( f"{body.position()} == {Float2(0.0, 0.0)}") 

    assert body.position() == Float2(0.0, 0.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in body.envelope() ]
    assert env == [(-0.5, 0.5), (0.5, 0.5), (0.5, -0.5), (-0.5, -0.5)]

    body.setShape( Shape().initializeRegular(0.5, 8) )
    env= [ ( round(x, 2), round(y, 2) ) for x, y in body.envelope() ]
    assert env == [(-0.23, 0.1), (-0.1, 0.23), (0.1, 0.23), (0.23, 0.1), (0.23, -0.1), (0.1, -0.23), (-0.1, -0.23), (-0.23, -0.1)]

    env= [ ( round(x, 2), round(y, 2) ) for x, y in body.envelope() ]
    assert env == [(-0.23, 0.1), (-0.1, 0.23), (0.1, 0.23), (0.23, 0.1), (0.23, -0.1), (0.1, -0.23), (-0.1, -0.23), (-0.23, -0.1)]

    body.position().set(1.0, 2.0)
    assert body.position() == Float2(1.0, 2.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in body.envelope() ]
    assert env == [(0.77, 2.1), (0.9, 2.23), (1.1, 2.23), (1.23, 2.1), (1.23, 1.9), (1.1, 1.77), (0.9, 1.77), (0.77, 1.9)]

def test_Body_init2():
    body= Body( 42, Float2(1.0, 2.0), Shape().initializeRegular(0.5, 8) )
    
    assert body.id() == 42
    assert body.position() == Float2(1.0, 2.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in body.envelope() ]
    assert env == [(0.77, 2.1), (0.9, 2.23), (1.1, 2.23), (1.23, 2.1), (1.23, 1.9), (1.1, 1.77), (0.9, 1.77), (0.77, 1.9)]
    
def test_Body_str():
    body= Body( 42, Float2(1.0, 2.0) )
    print(body)
    assert str(body) == "Body-42 ⌊(0.5, 1.5), (1.5, 2.5)⌉"

def test_Body_podable():
    body= Body( 42, Float2(1.0, 2.0) )
    pod= body.asPod()

    assert pod.numberOfWords() == 1
    assert pod.words() == ["Body"]
    assert pod.word() == "Body"
    assert pod.numberOfIntegers() == 2
    assert pod.integers() == [42, 0]
    assert pod.integer(1) == 42
    assert pod.integer(2) == 0
    assert pod.numberOfValues() == 2
    assert pod.values() == [1.0, 2.0]
    assert pod.value(1) == 1.0
    assert pod.value(2) == 2.0
    assert pod.numberOfChildren() == 1
    assert pod.children() == [ body.shape().asPod() ]


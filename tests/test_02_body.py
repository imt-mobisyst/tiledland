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

    body.setShape( Shape().setShapeRegular(0.5, 8) )
    env= [ ( round(x, 2), round(y, 2) ) for x, y in body.envelope() ]
    assert env == [(-0.23, 0.1), (-0.1, 0.23), (0.1, 0.23), (0.23, 0.1), (0.23, -0.1), (0.1, -0.23), (-0.1, -0.23), (-0.23, -0.1)]

    env= [ ( round(x, 2), round(y, 2) ) for x, y in body.envelope() ]
    assert env == [(-0.23, 0.1), (-0.1, 0.23), (0.1, 0.23), (0.23, 0.1), (0.23, -0.1), (0.1, -0.23), (-0.1, -0.23), (-0.23, -0.1)]

    body.position().set(1.0, 2.0)
    assert body.position() == Float2(1.0, 2.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in body.envelope() ]
    assert env == [(0.77, 2.1), (0.9, 2.23), (1.1, 2.23), (1.23, 2.1), (1.23, 1.9), (1.1, 1.77), (0.9, 1.77), (0.77, 1.9)]

def test_Body_init2():
    body= Body( 42, Float2(1.0, 2.0), Shape().setShapeRegular(0.5, 8) )
    
    assert body.id() == 42
    assert body.position() == Float2(1.0, 2.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in body.envelope() ]
    assert env == [(0.77, 2.1), (0.9, 2.23), (1.1, 2.23), (1.23, 2.1), (1.23, 1.9), (1.1, 1.77), (0.9, 1.77), (0.77, 1.9)]
    
def test_Body_str():
    body= Body( 42, Float2(1.0, 2.0) )
    print(body)
    assert str(body) == "Body-42 ⌊(0.5, 1.5), (1.5, 2.5)⌉"

def test_Body_absObj():
    body= Body( 42, Float2(1.0, 2.0) )

    assert body.numberOfWords() == 1
    assert body.wordAttributes() == ["Body"]
    assert body.wordAttribute() == "Body"
    assert body.numberOfInts() == 2
    assert body.intAttributes() == [42, 0]
    assert body.intAttribute(1) == 42
    assert body.intAttribute(2) == 0
    assert body.numberOfFloats() == 2
    assert body.floatAttributes() == [1.0, 2.0]
    assert body.floatAttribute(1) == 1.0
    assert body.floatAttribute(2) == 2.0
    assert body.numberOfChildren() == 1
    assert body.children() == [ body.shape() ]


# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from hacka.py  import Pod
from src.tiledland import Shape

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_Shape_init():
    
    shape= Shape()

    print( shape.envelope() )
    assert shape.envelope() == [(-0.5, 0.5), (0.5, 0.5), (0.5, -0.5), (-0.5, -0.5)]
    
    shape= Shape( 42.0 )
    assert shape.envelope() == [(-21.0, 21.0), (21.0, 21.0), (21.0, -21.0), (-21.0, -21.0)]

    shape.setShapeSquare( 2.0 )
    assert shape.envelope() == [(-1.0, 1.0), (1.0, 1.0), (1.0, -1.0), (-1.0, -1.0)]

def test_Shape_regular():
    shape= Shape().setShapeRegular( 20.0, 6 )
    assert len(shape.envelope()) == 6
    env= [ ( round(x, 2), round(y, 2) ) for x, y in shape.envelope() ]
    print( env )
    assert env == [
        (-8.66, 5.0), (-0.0, 10.0), (8.66, 5.0),
        (8.66, -5.0), (0.0, -10.0), (-8.66, -5.0)
    ]
    
    box= [ 
        (round(corner.x(), 2), round(corner.y(), 2))
        for corner in shape.box()
    ]
    assert box == [ (-8.66, -10.0), (8.66, 10.0) ]

    
def test_Shape_str():
    shape= Shape(10.0)
    print(f">>> {shape}")
    assert str(shape) == "Shape-4 [(-5.0, -5.0), (5.0, 5.0)]"
    shape.setShapeRegular( 20.0, 6 )
    print(f">>> {shape}")
    assert str(shape) == "Shape-6 [(-8.66, -10.0), (8.66, 10.0)]"

def test_Shape_podable():
    shape= Shape( 10.0 )

    assert shape.wordAttributes() == ["Shape"]
    assert shape.intAttributes() == []
    assert shape.floatAttributes() == [-5.0, 5.0, 5.0, 5.0, 5.0, -5.0, -5.0, -5.0]
    assert shape.children() == []

    shapeBis= Shape()
    assert shapeBis.envelope() == [(-0.5, 0.5), (0.5, 0.5), (0.5, -0.5), (-0.5, -0.5)]

    shapeBis.initializeFrom( shape )
    assert shapeBis.envelope() == [(-5.0, 5.0), (5.0, 5.0), (5.0, -5.0), (-5.0, -5.0)]

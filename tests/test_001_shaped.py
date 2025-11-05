# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland import Point, Polygon, Shaped

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_Shaped_init():
    shape= Shaped()

    assert( shape.numberOfVertex() == 0 )
    print( shape.asPoints() )
    assert( shape.asPoints() == [] )
    assert( shape.matter() == 0 )
    
def test_Shaped_init2():
    shape= Shaped().initializeSquare(1.0)
    assert shape.asZip() == [(-0.5, 0.5), (0.5, 0.5), (0.5, -0.5), (-0.5, -0.5)]
    assert( shape.asPoints() == [
        Point(-0.5, 0.5), Point(0.5, 0.5),
        Point(0.5, -0.5), Point(-0.5, -0.5)
    ])

    shape= Shaped().initializeSquare(42.0)
    assert shape.asZip() == [(-21.0, 21.0), (21.0, 21.0), (21.0, -21.0), (-21.0, -21.0)]

    shape.move( Point(-0.2, -8.7) )
    print( shape.asPoints() )
    assert( shape.asPoints() == [
        Point(-21.2, 12.3), Point(20.8, 12.3),
        Point(20.8, -29.7), Point(-21.2, -29.7)       
    ])

    shape.initializeSquare( 2.0 )
    assert shape.asZip() == [(-1.0, 1.0), (1.0, 1.0), (1.0, -1.0), (-1.0, -1.0)]
    
def test_Shaped_init3():
    shape= Shaped( [Point(-0.4, 0.6), Point(0.2, 0.8), Point(0.6, -0.6), Point(-0.5, -0.5)] )

    assert( str(shape.asPoints()) == "[<POINT (-0.4 0.6)>, <POINT (0.2 0.8)>, <POINT (0.6 -0.6)>, <POINT (-0.5 -0.5)>]" )
    assert( shape.centroid().distance( Point( 0.0, 0.02 ) ) < 0.01 )
    assert( shape.listXY() )
    assert shape.asRoundedZip() == [
        (-0.4, 0.6), (0.2, 0.8), (0.6, -0.6), (-0.5, -0.5)
    ]

    shape= Shaped().initializeListXY(
        [-0.4, 0.2, 0.6, -0.5, -0.4],
        [0.6, 0.8, -0.6, -0.5, 0.6]
    )
    assert shape.asRoundedZip() == [
        (-0.4, 0.6), (0.2, 0.8), (0.6, -0.6), (-0.5, -0.5)
    ]

def test_Shaped_regular():
    shape= Shaped().initializeRegular( 20.0, 6 )
    assert len( shape.asPoints() ) == 6
    env= [ ( round(x, 2), round(y, 2) ) for x, y in shape.asZip() ]
    print( env )
    assert env == [
        (-8.66, 5.0), (-0.0, 10.0), (8.66, 5.0),
        (8.66, -5.0), (0.0, -10.0), (-8.66, -5.0)
    ]
    
    box= shape.asBox()
    box.round(2)

    assert box.asList() == [-8.66, -10.0, 8.66, 10.0]
    assert box.asZip() == [ (-8.66, -10.0), (8.66, 10.0) ]

def test_Shaped_str():
    shape= Shaped().initializeSquare(10.0)
    print(f">>> {shape}")
    assert str(shape) == "Shape 4[(-5.0, -5.0), (5.0, 5.0)]"
    shape.initializeRegular(20.0, 6)
    print(f">>> {shape}")
    assert str(shape) == "Shape 6[(-8.66, -10.0), (8.66, 10.0)]"

def test_Shaped_podable():
    shape= Shaped().initializeSquare(10.0)
    pod= shape.asPod()
    
    assert pod.words() == ["Shape"]
    assert pod.integers() == []
    print( pod.values() )
    assert pod.values() == [-5.0, 5.0, 5.0, -5.0, 5.0, 5.0, -5.0, -5.0]
    assert pod.children() == []

    shBis= Shaped()
    assert shBis.asZip() == []

    shBis.fromPod( shape.asPod() )
    assert shBis.asZip() == [(-5.0, 5.0), (5.0, 5.0), (5.0, -5.0), (-5.0, -5.0)]

def test_Shaped_podCopy():
    Entity= Shaped().initializeSquare(0.9)
    assert Entity.asZip() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]
    
    EntityBis= Entity.copy()
    assert EntityBis.asZip() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]

def test_Shaped_podCopy():
    shape= Shaped().initializeSquare(0.9)
    assert shape.asZip() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]
    
    shBis= shape.podCopy()
    assert shBis.asZip() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]

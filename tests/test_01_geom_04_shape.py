# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland.geometry import Point, Shape

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_Shape_init():
    shape= Shape()

    print( shape.asZipped() )
    assert shape.asZipped() == []
    
def test_Shape_init2():
    shape= Shape().initializeSquare(1.0)

    print( shape.asZipped() )
    assert shape.asZipped() == [(-0.5, 0.5), (0.5, 0.5), (0.5, -0.5), (-0.5, -0.5)]
    
    shape= Shape().initializeSquare( 42.0 )
    assert shape.asZipped() == [(-21.0, 21.0), (21.0, 21.0), (21.0, -21.0), (-21.0, -21.0)]

    shape.initializeSquare( 2.0 )
    assert shape.asZipped() == [(-1.0, 1.0), (1.0, 1.0), (1.0, -1.0), (-1.0, -1.0)]
    
def test_Shape_init3():
    shape= Shape().fromZipped([(-0.4, 0.6), (0.2, 0.8), (0.6, -0.6), (-0.5, -0.5)])

    print( shape.asLists() )
    assert shape.asLists() == ([-0.4, 0.2, 0.6, -0.5], [0.6, 0.8, -0.6, -0.5])

    shape= Shape().fromLists(
        [-0.4, 0.2, 0.6, -0.5],
        [0.6, 0.8, -0.6, -0.5]
    )
    print( shape.asZipped() )
    assert shape.asZipped() == [(-0.4, 0.6), (0.2, 0.8), (0.6, -0.6), (-0.5, -0.5)]
    
def test_Shape_regular():
    shape= Shape().initializeRegular( 20.0, 6 )
    assert len(shape.asZipped()) == 6
    env= [ ( round(x, 2), round(y, 2) ) for x, y in shape.asZipped() ]
    print( env )
    assert env == [
        (-8.66, 5.0), (-0.0, 10.0), (8.66, 5.0),
        (8.66, -5.0), (0.0, -10.0), (-8.66, -5.0)
    ]
    
    box= shape.box()
    box.round(2)

    assert box.asList() == [-8.66, -10.0, 8.66, 10.0]
    assert box.asZip() == [ (-8.66, -10.0), (8.66, 10.0) ]

    
def test_Shape_str():
    shape= Shape().initializeSquare(10.0)
    print(f">>> {shape}")
    assert str(shape) == "Shape 4[(-5.0, -5.0), (5.0, 5.0)]"
    shape.initializeRegular( 20.0, 6 )
    print(f">>> {shape}")
    assert str(shape) == "Shape 6[(-8.66, -10.0), (8.66, 10.0)]"

def test_Shape_podable():
    shape= Shape().initializeSquare( 10.0 )
    pod= shape.asPod()

    assert pod.words() == ["Shape"]
    assert pod.integers() == []
    assert pod.values() == [-5.0, 5.0, 5.0, 5.0, 5.0, -5.0, -5.0, -5.0]
    assert pod.children() == []

    shapeBis= Shape()
    assert shapeBis.asZipped() == []

    shapeBis.fromPod( shape.asPod() )
    assert shapeBis.asZipped() == [(-5.0, 5.0), (5.0, 5.0), (5.0, -5.0), (-5.0, -5.0)]

def test_Shape_podCopy():
    shape= Shape().initializeSquare(0.9)
    assert shape.asZipped() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]
    
    shapeBis= shape.copy()
    assert shapeBis.asZipped() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]

def test_Shape_podCopy():
    shape= Shape().initializeSquare(0.9)
    assert shape.asZipped() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]
    
    shapeBis= shape.podCopy()
    assert shapeBis.asZipped() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]

def test_Shape_convex():
    shape= Shape().initializeSquare(0.9)
    assert shape.asZipped() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45)]
    
    convex= shape.asConvex()
    print( f"Convex : {convex.asZipped()}" )
    assert convex.asZipped() == [(-0.45, -0.45), (-0.45, 0.45), (0.45, 0.45), (0.45, -0.45)]
    
    shape= Shape([
        Point(1.0, 1.0),
        Point(4.5, 3.0),
        Point(6.0, 0.5),
        Point(1.5, 4.0),
        Point(4.5, 4.5),
        Point(2.5, 2.0)
    ])

    convex= shape.asConvex()
    print( f"Convex : {convex.asZipped()}" )
    assert convex.asZipped() == [(1.0, 1.0), (1.5, 4.0), (4.5, 4.5), (6.0, 0.5)]
    
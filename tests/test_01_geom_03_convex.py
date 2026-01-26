# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland.geometry import Point, Line, Convex, Box

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_Convex_init():
    shape= Convex()

    print( shape.asZipped() )
    assert shape.asZipped() == []
    
def test_Convex_init2():
    shape= Convex().initializeSquare(1.0)

    print( shape.asZipped() )
    assert shape.asZipped() == [(-0.5, 0.5), (0.5, 0.5), (0.5, -0.5), (-0.5, -0.5)]
    
    shape= Convex().initializeSquare( 42.0 )
    assert shape.asZipped() == [(-21.0, 21.0), (21.0, 21.0), (21.0, -21.0), (-21.0, -21.0)]

    shape.initializeSquare( 2.0 )
    assert shape.asZipped() == [(-1.0, 1.0), (1.0, 1.0), (1.0, -1.0), (-1.0, -1.0)]
    
def test_Convex_init3():
    shape= Convex().fromZipped([(-0.4, 0.6), (0.2, 0.8), (0.6, -0.6), (-0.5, -0.5)])

    print( shape.asLists() )
    assert shape.asLists() == ([-0.4, 0.2, 0.6, -0.5], [0.6, 0.8, -0.6, -0.5])

    shape= Convex().fromLists(
        [-0.4, 0.2, 0.6, -0.5],
        [0.6, 0.8, -0.6, -0.5]
    )
    print( shape.asZipped() )
    assert shape.asZipped() == [(-0.4, 0.6), (0.2, 0.8), (0.6, -0.6), (-0.5, -0.5)]
    
def test_Convex_regular():
    shape= Convex().initializeRegular( 20.0, 6 )
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

    
def test_Convex_str():
    shape= Convex().initializeSquare(10.0)
    print(f">>> {shape}")
    assert str(shape) == "Convex 4[(-5.0, -5.0), (5.0, 5.0)]"
    shape.initializeRegular( 20.0, 6 )
    print(f">>> {shape}")
    assert str(shape) == "Convex 6[(-8.66, -10.0), (8.66, 10.0)]"

def test_Convex_podable():
    shape= Convex().initializeSquare( 10.0 )
    pod= shape.asPod()

    assert pod.words() == ["Convex"]
    assert pod.integers() == []
    assert pod.values() == [-5.0, 5.0, 5.0, 5.0, 5.0, -5.0, -5.0, -5.0]
    assert pod.children() == []

    shapeBis= Convex()
    assert shapeBis.asZipped() == []

    shapeBis.fromPod( shape.asPod() )
    assert shapeBis.asZipped() == [(-5.0, 5.0), (5.0, 5.0), (5.0, -5.0), (-5.0, -5.0)]

def test_Convex_podCopy():
    shape= Convex().initializeSquare(0.9)
    assert shape.asZipped() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]
    
    shapeBis= shape.copy()
    assert shapeBis.asZipped() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]

def test_Convex_podCopy():
    shape= Convex().initializeSquare(0.9)
    assert shape.asZipped() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]
    
    shapeBis= shape.podCopy()
    assert shapeBis.asZipped() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]

def test_Convex_convex():
    shape= Convex().initializeSquare(0.9)
    assert shape.asZipped() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45)]
    
    convex= shape.asConvex()
    print( f"Convex : {convex.asZipped()}" )
    assert convex.asZipped() == [(-0.45, -0.45), (-0.45, 0.45), (0.45, 0.45), (0.45, -0.45)]
    
    shape= Convex([
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
    
def test_shape_distance():
    shape= Convex([
        Point(5.0, 1.0),
        Point(5.0, 4.0),
        Point(12.0, 4.5)
    ])
    p= Point(3.0, 2.5)
    distance= round( shape.distancePoint(p), 3 )
    assert distance == 2.0

    shape= Convex([
        Point(8.0, 1.0),
        Point(5.0, 2.5),
        Point(8.5, 4.5)
    ])
    p= Point(3.0, 2.5)
    distance= round( shape.distancePoint(p), 3 )
    assert distance == 2.0

    shape= Convex([
        Point(1.0, 1.0),
        Point(1.5, 4.0),
        Point(4.5, 4.5),
        Point(6.0, 0.5)
    ])
    p= Point(0.0, 0.0)
    distance= round( shape.distancePoint(p), 3 )
    assert distance == 1.414

    p= Point(4.5, 3.0)
    distance= round( shape.distancePoint(p), 3 )
    assert distance == 0.527

    shape= Convex([
        Point(1.0, 1.0),
        Point(5.5, 5.0),
        Point(6.0, 0.5)
    ])

    assert round( shape.distancePoint( Point(1.0, 1.0) ), 3 ) == 0.00
    assert round( shape.distancePoint( Point(0.0, 1.0) ), 3 ) == 1.00
    assert round( shape.distancePoint( Point(1.0, 5.5) ), 3 ) == 3.363
    assert round( shape.distancePoint( Point(4.4, 2.5) ), 3 ) == 1.138

    assert round( shape.distanceLine( Line(Point(1.0, 1.0), Point(0.0, 0.0))), 3 ) == 0.00
    assert round( shape.distanceLine( Line(Point(0.0, 1.0), Point(0.0, 0.0))), 3 ) == 1.00
    assert round( shape.distanceLine( Line(Point(1.0, 5.5), Point(-3.0, 4.0))), 3 ) == 3.363
    assert round( shape.distanceLine( Line(Point(4.4, 2.5), Point(0.0, 0.0))), 3 ) == 1.138

    assert round( shape.distance( Convex([
            Point(7.0, 0.5), Point(12.5, 5.0), Point(13.0, 0.5)
            ])
        ), 3 ) == 1.0
    assert round( shape.distance( Convex([
            Point(6.0, 0.5), Point(12.5, 5.0), Point(13.0, 0.5)
            ])
        ), 3 ) == 0.0
    assert round( shape.distance( Convex([
            Point(4.5, 2.5), Point(12.5, 5.0), Point(13.0, 0.5)
            ])
        ), 3 ) == 0.0
    
    assert round( shape.distance( Convex([
            Point(1.0, 2.0), Point(1.0, 5.5), Point(4.5, 5.0)
            ])
        ), 3 ) == 0.664
    
    
def test_box_colision():
    b= Box( [Point(3, 0.5), Point(7, 3.5)] )

    assert not b.isColliding( Box([Point(1, 1.5), Point(2, 5)]) )
    assert b.isColliding( Box([Point(1.5, 1), Point(5, 4.5)]) )
    assert b.isColliding( Box([Point(3.5, 1.0), Point(4.5, 2)]) )

    assert not b.isIncluding( Box([Point(1, 1.5), Point(2, 5)]) )
    assert not b.isIncluding( Box([Point(1.5, 1), Point(5, 4.5)]) )
    assert b.isIncluding( Box([Point(3.5, 1.0), Point(4.5, 2)]) )

def test_shape_inclusion():
    shape= Convex([
        Point(1.0, 1.0),
        Point(6.0, 11.0),
        Point(10.0, 1.5)
    ])
    
    assert not shape.isIncludingPoint( Point(0.0, 0.0) )
    assert shape.isIncludingPoint( Point(4.5, 3.0) )

    shape= Convex([
        Point(1.0, 1.0),
        Point(5.5, 5.0),
        Point(6.0, 0.5)
    ])
    
    assert not shape.isIncludingPoint( Point(0.0, 0.0) )
    assert not shape.isIncludingPoint( Point(2.0, 3.0) )
    assert shape.isIncludingPoint( Point(1.0, 1.0) )
    assert shape.isIncludingPoint( Point(4.0, 2.0) )

    assert not shape.isIncludingLine(Line( Point(2.0, 3.0), Point(0.0, 0.0) ))
    assert not shape.isIncludingLine(Line( Point(2.0, 3.0), Point(1.0, 1.0) ))
    assert shape.isIncludingLine(Line( Point(1.0, 1.0), Point(4.0, 2.0) ))

def test_shape_colision():
    shape= Convex([
        Point(1.0, 1.0),
        Point(5.5, 5.0),
        Point(6.0, 0.5)
    ])

    assert not shape.isCollidingLine(Line( Point(0.0, 0.0), Point(0.0, 4.0) ))
    assert not shape.isCollidingLine(Line( Point(2.0, 3.0), Point(3.5, 4.5) ))
    assert shape.isCollidingLine(Line( Point(2.0, 3.0), Point(4, 2) ))
    assert shape.isCollidingLine(Line( Point(2.0, 3.0), Point(7, 4) ))

    assert not shape.isColliding( Convex([
        Point(7.0, 1.0), Point(12.5, 5.0), Point(13.0, 0.5)
    ]) )
    assert not shape.isColliding( Convex([
        Point(1.0, 2.0), Point(4, 5), Point(0.5, 5.5)
    ]) )
    assert shape.isColliding( Convex([
        Point(1.0, 2.0), Point(4, 5), Point(5, 2.5)
    ]) )
    assert shape.isColliding( Convex([
        Point(1.0, 2.0), Point(4, 5), Point(5, 2.5)
    ]) )
    assert shape.isColliding( Convex([
        Point(1.0, 2.0), Point(4, 5), Point(8, 3)
    ]) )
    assert shape.isColliding( Convex([
        Point(1.0, 1.0), Point(5.5, 5.0), Point(6.0, 0.5)
    ]) )

def test_shape_union_intersection():
    pass # ToDo

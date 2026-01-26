# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland.geometry import Point, Line, Convex, Box

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_Convex_init():
    convex= Convex()

    print( convex.asZipped() )
    assert convex.asZipped() == []
    
def test_Convex_initSquare():
    convex= Convex().initializeSquare(1.0)

    print( convex.asZipped() )
    assert convex.asZipped() == [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)]
    
    convex= Convex().initializeSquare( 42.0 )
    assert convex.asZipped() == [(-21.0, -21.0), (-21.0, 21.0), (21.0, 21.0), (21.0, -21.0)]

    convex.initializeSquare( 2.0 )
    assert convex.asZipped() == [(-1.0, -1.0), (-1.0, 1.0), (1.0, 1.0), (1.0, -1.0)]
  
def test_Convex_initRegular():
    convex= Convex().initializeRegular( 20.0, 6 )
    assert len(convex.asZipped()) == 6
    env= [ ( round(x, 2), round(y, 2) ) for x, y in convex.asZipped() ]
    print( env )
    assert env == [
        (-8.66, 5.0), (-0.0, 10.0), (8.66, 5.0),
        (8.66, -5.0), (0.0, -10.0), (-8.66, -5.0)
    ]
    
    box= convex.box()
    box.round(2)

    assert box.asList() == [-8.66, -10.0, 8.66, 10.0]
    assert box.asZip() == [ (-8.66, -10.0), (8.66, 10.0) ]

def test_Convex_forcePoint():
    convex= Convex().forcePoints([
        Point(-0.4, 0.6), Point(0.2, 0.8), Point(0.6, -0.6), Point(-0.5, -0.5)
    ])
    
    print( convex.asZipped() )
    assert convex.asZipped() == [(-0.4, 0.6), (0.2, 0.8), (0.6, -0.6), (-0.5, -0.5)]

def test_Convex_str():
    convex= Convex().initializeSquare(10.0)
    print(f">>> {convex}")
    assert str(convex) == "Convex 4[(-5.0, -5.0), (5.0, 5.0)]"
    convex.initializeRegular( 20.0, 6 )
    print(f">>> {convex}")
    assert str(convex) == "Convex 6[(-8.66, -10.0), (8.66, 10.0)]"

def test_Convex_podable():
    convex= Convex().initializeSquare( 10.0 )
    pod= convex.asPod()

    assert pod.words() == ["Convex"]
    assert pod.integers() == []
    assert pod.values() == [-5.0, -5.0, -5.0, 5.0, 5.0, 5.0, 5.0, -5.0]
    assert pod.children() == []

    convexBis= Convex()
    assert convexBis.asZipped() == []

    convexBis.fromPod( convex.asPod() )
    assert convexBis.asZipped() == [(-5.0, -5.0), (-5.0, 5.0), (5.0, 5.0), (5.0, -5.0)]

def test_Convex_podCopy():
    convex= Convex().initializeSquare(0.9)
    assert convex.asZipped() == [(-0.45, -0.45), (-0.45, 0.45), (0.45, 0.45), (0.45, -0.45)]
    
    convexBis= convex.copy()
    assert convexBis.asZipped() == [(-0.45, -0.45), (-0.45, 0.45), (0.45, 0.45), (0.45, -0.45)]

def test_Convex_podCopy():
    convex= Convex().initializeSquare(0.9)
    assert convex.asZipped() == [(-0.45, -0.45), (-0.45, 0.45), (0.45, 0.45), (0.45, -0.45)]
    
    convexBis= convex.podCopy()
    assert convexBis.asZipped() == [(-0.45, -0.45), (-0.45, 0.45), (0.45, 0.45), (0.45, -0.45)]

def test_Convex_convex():
    convex= Convex().initializeSquare(0.9)
    assert convex.asZipped() == [(-0.45, -0.45), (-0.45, 0.45), (0.45, 0.45), (0.45, -0.45)]

    removed= convex.makeConvex()
    assert removed == []
    assert convex.asZipped() == [(-0.45, -0.45), (-0.45, 0.45), (0.45, 0.45), (0.45, -0.45)]
    
    convex= Convex().forcePoints([
        Point(1.0, 1.0),
        Point(4.5, 3.0),
        Point(6.0, 0.5),
        Point(1.5, 4.0),
        Point(4.5, 4.5),
        Point(2.5, 2.0)
    ])

    removed= convex.makeConvex()
    removed= [ (p.x(), p.y()) for p in removed ]
    print( f"Convex : {convex.asZipped()}" )
    assert convex.asZipped() == [(1.0, 1.0), (1.5, 4.0), (4.5, 4.5), (6.0, 0.5)]
    assert removed == [(2.5, 2.0), (4.5, 3.0)]

def test_Convex_fromCoord():
    convex= Convex().fromZipped([(-0.4, 0.6), (0.2, 0.8), (0.6, -0.6), (-0.5, -0.5)])
    
    print( convex.asLists() )
    assert convex.asLists() == ([-0.5, -0.4, 0.2, 0.6], [-0.5, 0.6, 0.8, -0.6])

    convex= Convex().fromLists(
        [-0.4, 0.2, 0.6, -0.5],
        [0.6, 0.8, -0.6, -0.5]
    )
    print( convex.asZipped() )
    assert convex.asZipped() == [(-0.5, -0.5), (-0.4, 0.6), (0.2, 0.8), (0.6, -0.6)]

def test_convex_distance():
    convex= Convex([
        Point(5.0, 1.0),
        Point(5.0, 4.0),
        Point(12.0, 4.5)
    ])
    p= Point(3.0, 2.5)
    distance= round( convex.distancePoint(p), 3 )
    assert distance == 2.0

    convex= Convex([
        Point(8.0, 1.0),
        Point(5.0, 2.5),
        Point(8.5, 4.5)
    ])
    p= Point(3.0, 2.5)
    distance= round( convex.distancePoint(p), 3 )
    assert distance == 2.0

    convex= Convex([
        Point(1.0, 1.0),
        Point(1.5, 4.0),
        Point(4.5, 4.5),
        Point(6.0, 0.5)
    ])
    p= Point(0.0, 0.0)
    distance= round( convex.distancePoint(p), 3 )
    assert distance == 1.414

    p= Point(4.5, 3.0)
    distance= round( convex.distancePoint(p), 3 )
    assert distance == 0.527

    convex= Convex([
        Point(1.0, 1.0),
        Point(5.5, 5.0),
        Point(6.0, 0.5)
    ])

    assert round( convex.distancePoint( Point(1.0, 1.0) ), 3 ) == 0.00
    assert round( convex.distancePoint( Point(0.0, 1.0) ), 3 ) == 1.00
    assert round( convex.distancePoint( Point(1.0, 5.5) ), 3 ) == 3.363
    assert round( convex.distancePoint( Point(4.4, 2.5) ), 3 ) == 1.138

    assert round( convex.distanceLine( Line(Point(1.0, 1.0), Point(0.0, 0.0))), 3 ) == 0.00
    assert round( convex.distanceLine( Line(Point(0.0, 1.0), Point(0.0, 0.0))), 3 ) == 1.00
    assert round( convex.distanceLine( Line(Point(1.0, 5.5), Point(-3.0, 4.0))), 3 ) == 3.363
    assert round( convex.distanceLine( Line(Point(4.4, 2.5), Point(0.0, 0.0))), 3 ) == 0.375

    assert round( convex.distance( Convex([
            Point(7.0, 0.5), Point(12.5, 5.0), Point(13.0, 0.5)
            ])
        ), 3 ) == 1.0
    assert round( convex.distance( Convex([
            Point(6.0, 0.5), Point(12.5, 5.0), Point(13.0, 0.5)
            ])
        ), 3 ) == 0.0
    assert round( convex.distance( Convex([
            Point(4.5, 2.5), Point(12.5, 5.0), Point(13.0, 0.5)
            ])
        ), 3 ) == 0.0
    
    assert round( convex.distance( Convex([
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

def test_convex_inclusion():
    convex= Convex([
        Point(1.0, 1.0),
        Point(6.0, 11.0),
        Point(10.0, 1.5)
    ])
    
    assert not convex.isIncludingPoint( Point(0.0, 0.0) )
    assert convex.isIncludingPoint( Point(4.5, 3.0) )

    convex= Convex([
        Point(1.0, 1.0),
        Point(5.5, 5.0),
        Point(6.0, 0.5)
    ])
    
    assert not convex.isIncludingPoint( Point(0.0, 0.0) )
    assert not convex.isIncludingPoint( Point(2.0, 3.0) )
    assert convex.isIncludingPoint( Point(1.0, 1.0) )
    assert convex.isIncludingPoint( Point(4.0, 2.0) )

    assert not convex.isIncludingLine(Line( Point(2.0, 3.0), Point(0.0, 0.0) ))
    assert not convex.isIncludingLine(Line( Point(2.0, 3.0), Point(1.0, 1.0) ))
    assert convex.isIncludingLine(Line( Point(1.0, 1.0), Point(4.0, 2.0) ))

def test_convex_colision():
    convex= Convex([
        Point(1.0, 1.0),
        Point(5.5, 5.0),
        Point(6.0, 0.5)
    ])

    assert not convex.isCollidingLine(Line( Point(0.0, 0.0), Point(0.0, 4.0) ))
    assert not convex.isCollidingLine(Line( Point(2.0, 3.0), Point(3.5, 4.5) ))
    assert convex.isCollidingLine(Line( Point(2.0, 3.0), Point(4, 2) ))
    assert convex.isCollidingLine(Line( Point(2.0, 3.0), Point(7, 4) ))

    assert not convex.isColliding( Convex([
        Point(7.0, 1.0), Point(12.5, 5.0), Point(13.0, 0.5)
    ]) )
    assert not convex.isColliding( Convex([
        Point(1.0, 2.0), Point(4, 5), Point(0.5, 5.5)
    ]) )
    assert convex.isColliding( Convex([
        Point(1.0, 2.0), Point(4, 5), Point(5, 2.5)
    ]) )
    assert convex.isColliding( Convex([
        Point(1.0, 2.0), Point(4, 5), Point(5, 2.5)
    ]) )
    assert convex.isColliding( Convex([
        Point(1.0, 2.0), Point(4, 5), Point(8, 3)
    ]) )
    assert convex.isColliding( Convex([
        Point(1.0, 1.0), Point(5.5, 5.0), Point(6.0, 0.5)
    ]) )

def test_convex_mergeFull():
    convex= Convex([
        Point(1.0, 1.0),
        Point(5.5, 5.0),
        Point(6.0, 0.5)
    ])
    
    convbis= Convex([
        Point(6.5, 5.0),
        Point(9.0, 4.5),
        Point(8.5, 1.5)
    ])

    removed= convex.merge(convbis)

    print( convex.asZipped() )
    assert convex.asZipped() == [
        (1.0, 1.0), (5.5, 5.0),
        (6.5, 5.0), (9.0, 4.5), (8.5, 1.5),
        (6.0, 0.5)
    ]
    assert removed == []

def test_convex_mergeFull():
    convex= Convex([
        Point(1.0, 1.0),
        Point(5.5, 5.0),
        Point(6.0, 0.5)
    ])
    
    convbis= Convex([
        Point(6.5, 5.0),
        Point(9.0, 4.5),
        Point(8.5, 1.5)
    ])

    removed= convex.merge(convbis)

    print( convex.asZipped() )
    assert convex.asZipped() == [
        (1.0, 1.0), (5.5, 5.0),
        (6.5, 5.0), (9.0, 4.5), (8.5, 1.5),
        (6.0, 0.5)
    ]
    assert removed == []

def test_convex_merge2():
    convex= Convex([
        Point(1.0, 1.0),
        Point(5.5, 5.0),
        Point(6.0, 0.5)
    ])
    
    convbis= Convex([
        Point(6.5, 3.0),
        Point(9.0, 4.5),
        Point(8.5, 1.5)
    ])

    removed= convex.merge(convbis)

    print( convex.asZipped() )
    assert convex.asZipped() == [
        (1.0, 1.0), (5.5, 5.0),
        (9.0, 4.5), (8.5, 1.5),
        (6.0, 0.5)
    ]
    assert [(p.x(), p.y()) for p in removed] == [(6.5, 3.0)]

def test_convex_mergeFull():
    convex= Convex([
        Point(1.0, 1.0),
        Point(5.5, 5.0),
        Point(6.0, 0.5)
    ])
    
    convbis= Convex([
        Point(6.5, 5.0),
        Point(9.0, 4.5),
        Point(8.5, 1.5)
    ])

    removed= convex.merge(convbis)

    print( convex.asZipped() )
    assert convex.asZipped() == [
        (1.0, 1.0), (5.5, 5.0),
        (6.5, 5.0), (9.0, 4.5), (8.5, 1.5),
        (6.0, 0.5)
    ]
    assert removed == []

def test_convex_merge2():
    convex= Convex([
        Point(1.0, 1.0),
        Point(5.5, 5.0),
        Point(6.0, 0.5)
    ])
    
    convbis= Convex([
        Point(4.5, 2.5),
        Point(9.0, 4.5),
        Point(8.5, 1.5)
    ])

    removed= convex.merge(convbis)

    print( convex.asZipped() )
    assert convex.asZipped() == [
        (1.0, 1.0), (5.5, 5.0),
        (9.0, 4.5), (8.5, 1.5),
        (6.0, 0.5)
    ]
    assert [(p.x(), p.y()) for p in removed] == [(4.5, 2.5)]

def test_convex_mergeInside():
    convex= Convex([
        Point(1.0, 1.0),
        Point(5.5, 5.0),
        Point(6.0, 0.5)
    ])
    
    convbis= Convex([
        Point(4.5, 2.5),
        Point(9.0, 4.5),
        Point(8.5, 1.5)
    ])

    removed= convex.merge(convbis)

    print( convex.asZipped() )
    assert convex.asZipped() == [
        (1.0, 1.0), (5.5, 5.0),
        (9.0, 4.5), (8.5, 1.5),
        (6.0, 0.5)
    ]
    assert [(p.x(), p.y()) for p in removed] == [(4.5, 2.5)]

def test_convex_mergeInsideBis():
    convex= Convex([
        Point(1.0, 1.0),
        Point(5.5, 5.0),
        Point(6.0, 0.5)
    ])
    
    convbis= Convex([
        Point(4.5, 2.5),
        Point(9.0, 4.5),
        Point(8.5, 1.5)
    ])

    removed= convbis.merge(convex)

    print( convbis.asZipped() )
    assert convbis.asZipped() == [
        (1.0, 1.0), (5.5, 5.0),
        (9.0, 4.5), (8.5, 1.5),
        (6.0, 0.5)
    ]
    assert [(p.x(), p.y()) for p in removed] == [(4.5, 2.5)]


def test_convex_mergeOnlyOne():
    convex= Convex([
        Point(1.0, 1.0),
        Point(5.5, 5.0),
        Point(6.0, 0.5)
    ])
    
    convbis= Convex([
        Point(6.0, 4.5),
        Point(8.0, 5.5),
        Point(6.5, 3.0)
    ])

    removed= convbis.merge(convex)

    print( convbis.asZipped() )
    assert convbis.asZipped() == [
        (1.0, 1.0), (5.5, 5.0),
        (8.0, 5.5),
        (6.0, 0.5)
    ]
    assert [(p.x(), p.y()) for p in removed] == [(6.5, 3.0), (6.0, 4.5)]


def test_convex_mergeNoOne():
    convex= Convex([
        Point(1.0, 1.0),
        Point(5.5, 5.0),
        Point(6.0, 0.5)
    ])
    
    convbis= Convex([
        Point(3.0, 1.5),
        Point(4.5, 2.5),
        Point(5.0, 1.0)
    ])

    removed= convbis.merge(convex)

    print( convbis.asZipped() )
    assert convbis.asZipped() == [
        (1.0, 1.0), (5.5, 5.0), (6.0, 0.5)
    ]
    assert( [(p.x(), p.y()) for p in removed]
           == [(3.0, 1.5), (5.0, 1.0), (4.5, 2.5)] )

    for p, ref in zip( removed, [0.697, 0.398, 1.204] ) :
        dist= convbis.distancePoint(p)
        assert round(dist, 3) == ref

    

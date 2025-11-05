from shapely.geometry import Point, Polygon

def test_shapely_point() :
    p= Point(0.0, 0.0)
    assert( str(p) == 'POINT (0 0)' )
    assert( p.x == 0.0 )
    assert( p.y == 0.0 )

    assert( p.distance( Point(0.0, 0.0) ) == 0.0 )
    assert( p.distance( Point(1.0, 0.0) ) == 1.0 )
    assert( round( p.distance( Point(1.0, 0.8) ), 4 ) == 1.2806 )

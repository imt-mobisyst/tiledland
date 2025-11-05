from shapely.geometry import Point, Polygon

def test_shapely_point() :
    p= Point(0.0, 0.0)
    assert( str(p) == 'POINT (0 0)' )
    assert( p.x == 0.0 )
    assert( p.y == 0.0 )

    assert( p.distance( Point(0.0, 0.0) ) == 0.0 )
    assert( p.distance( Point(1.0, 0.0) ) == 1.0 )
    assert( round( p.distance( Point(1.0, 0.8) ), 4 ) == 1.2806 )

def test_shapely_pointIneritence() :
    class P(Point): 
        def ok(self):
            return True
    p= P(0.0, 0.0)

    assert( type(p) != P )
    

def test_shapely_polygon() :
    poly= Polygon([(1.0, 0.0), (3.4, 8.7), (6.9, 0.5)])
    print( poly )
    assert( str(poly) == "POLYGON ((1 0, 3.4 8.7, 6.9 0.5, 1 0))" )
    

    print( poly.exterior.xy )

    assert(False)
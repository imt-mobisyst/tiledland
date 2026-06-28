import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src import tiledland as tll
from src.tiledland.geometry import Point

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_fast_load_local_tllcore():
    anEntity= tll.Entity()
    anAgent= tll.Agent()
    aTile= tll.Tile()
    aMap= tll.Map()

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - E N T I T Y
# ------------------------------------------------------------------------ #

def test_fast_entity_init():
    ent= tll.Entity()
    assert type( ent ) == tll.Entity

    assert type( ent.referenceShape() ) == tll.geometry.Convex
    assert type( ent.body() ) == tll.geometry.Convex

    points= [ str(p) for p in ent.referenceShape().points() ]
    print( points )
    assert points == ['(-0.43, -0.25)', '(-0.43, 0.25)', '(0.0, 0.5)', '(0.5, 0.0)', '(0.0, -0.5)']
    
    assert ent.orientation() == 0.0
    assert ent.position().asTuple() == (0.0, 0.0)

    bodyPoints= [ str(p) for p in ent.body().points() ]
    assert points == bodyPoints

def test_fast_entity_transform():
    ent= tll.Entity()

    ent.rotate( 1.67 )
    ent.translate( Point(1.5, -2.0) )

    artist= tll.createArtistSVG("shot-test.svg", 800, 600)
    artist.drawConvex( ent.referenceShape(), tll.artist.palette.foreground[3] )
    artist.drawConvex( ent.body(), tll.artist.palette.foreground[5] )
    artist.flip()

    assert ent.orientation() == 1.67
    assert ent.position().asTuple() == (1.5, -2.0)

    points= [ str(p) for p in ent.referenceShape().points() ]
    print( f"> reference : {points}" )
    assert points == ['(-0.43, -0.25)', '(-0.43, 0.25)', '(0.0, 0.5)', '(0.5, 0.0)', '(0.0, -0.5)']
    
    bodyPoints= [ str(p) for p in ent.body().points() ]
    print( f"> transfom  : {bodyPoints}" )
    assert bodyPoints == ['(1.79, -2.41)', '(1.29, -2.46)', '(1.0, -2.05)', '(1.45, -1.5)', '(2.0, -1.95)']

    ent.setPose( Point(0.0, 0.0), 0.0 )

    bodyPoints= [ str(p) for p in ent.body().points() ]
    print( f"> return  : {bodyPoints}" )
    assert bodyPoints == ['(-0.43, -0.25)', '(-0.43, 0.25)', '(0.0, 0.5)', '(0.5, 0.0)', '(0.0, -0.5)']

    ent.translate( Point(1.5, -2.0) )
    ent.rotate( 1.67 )

    assert ent.orientation() == 1.67
    assert ent.position().asTuple() == (1.5, -2.0)

    bodyPoints= [ str(p) for p in ent.body().points() ]
    print( f"> transfom2 : {bodyPoints}" )
    assert bodyPoints == ['(1.79, -2.41)', '(1.29, -2.46)', '(1.0, -2.05)', '(1.45, -1.5)', '(2.0, -1.95)']


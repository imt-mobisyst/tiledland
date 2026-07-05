import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src import tiledland as tll
from src.tiledland.geometry import Point

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_fast_load_local_tllcore():
    anAbsEntity= tll.AbsEntity()
    anEntity= tll.Entity()
    aTile= tll.Tile()
    aMap= tll.Map()

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - E N T I T Y
# ------------------------------------------------------------------------ #

def test_fast_entity_init():
    ent= tll.Entity()
    assert type( ent ) == tll.Entity

    assert type( ent.referenceShape() ) == tll.geometry.Convex
    assert type( ent.projectedShape() ) == tll.geometry.Convex

    points= [ str(p) for p in ent.referenceShape().points() ]
    print( points )
    assert points == ['(-0.43, -0.25)', '(-0.43, 0.25)', '(0.0, 0.5)', '(0.5, 0.0)', '(0.0, -0.5)']
    
    assert ent.orientation() == 0.0
    assert ent.position().asTuple() == (0.0, 0.0)

    bodyPoints= [ str(p) for p in ent.projectedShape().points() ]
    assert points == bodyPoints


def test_fast_entity_init2():
    entity= tll.Entity()

    assert type(entity) == tll.Entity
    assert entity.index() == 0
    print( f"{entity.position()} == {Point(0.0, 0.0)}") 

    assert entity.position() == Point(0.0, 0.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in entity.projectedShape().asZipped() ]
    
    print( env ) 
    assert env == [(-0.43, -0.25), (-0.43, 0.25), (0.0, 0.5), (0.5, 0.0), (0.0, -0.5)]

    entity.setReferenceShape( tll.Convex().initRegular(0.5, 8) )
    env= [ ( round(x, 2), round(y, 2) ) for x, y in entity.projectedShape().asZipped() ]
    print( env )
    assert env == [(-0.23, -0.1), (-0.23, 0.1), (-0.1, 0.23), (0.1, 0.23), (0.23, 0.1), (0.23, -0.1), (0.1, -0.23), (-0.1, -0.23)]

    entity.setPosition(1.0, 2.0)
    assert entity.position() == Point(1.0, 2.0)
    env= [ ( round(x, 2), round(y, 2) ) for x, y in entity.projectedShape().asZipped() ]
    print( env )
    assert env == [(0.77, 1.9), (0.77, 2.1), (0.9, 2.23), (1.1, 2.23), (1.23, 2.1), (1.23, 1.9), (1.1, 1.77), (0.9, 1.77)]


def test_fast_entity_init3():
    entity= tll.Entity(
        0, tll.Convex().initRegular(0.5, 8),
        Point(1.0, 2.0), 0.4,
        tll.Brush(), 12, 42 )

    assert entity.area() == 12
    assert entity.index() == 42
    assert entity.location() == (12, 42)
    assert entity.position() == Point(1.0, 2.0)
    assert entity.orientation() == 0.4

    env= [ ( round(x, 2), round(y, 2) ) for x, y in entity.referenceShape().asZipped() ]
    print( env )
    assert env == [(-0.23, -0.1), (-0.23, 0.1), (-0.1, 0.23), (0.1, 0.23), (0.23, 0.1), (0.23, -0.1), (0.1, -0.23), (-0.1, -0.23)]
    
    env= [ ( round(x, 2), round(y, 2) ) for x, y in entity.projectedShape().asZipped() ]
    print( env )
    assert env == [(0.82, 1.82), (0.75, 2.0), (0.82, 2.18), (1.0, 2.25), (1.18, 2.18), (1.25, 2.0), (1.18, 1.82), (1.0, 1.75)]
    
def test_fast_entity_transform():
    ent= tll.Entity()

    ent.rotate( 1.67 )
    ent.translate( Point(1.5, -2.0) )

    artist= tll.createArtistSVG("shot-test.svg", 800, 600)
    artist.drawConvex( ent.referenceShape(), tll.artist.palette.foreground[3] )
    artist.drawConvex( ent.projectedShape(), tll.artist.palette.foreground[5] )
    artist.flip()

    assert ent.orientation() == 1.67
    assert ent.position().asTuple() == (1.5, -2.0)

    points= [ str(p) for p in ent.referenceShape().points() ]
    print( f"> reference : {points}" )
    assert points == ['(-0.43, -0.25)', '(-0.43, 0.25)', '(0.0, 0.5)', '(0.5, 0.0)', '(0.0, -0.5)']
    
    bodyPoints= [ str(p) for p in ent.projectedShape().points() ]
    print( f"> transfom  : {bodyPoints}" )
    assert bodyPoints == ['(1.79, -2.41)', '(1.29, -2.46)', '(1.0, -2.05)', '(1.45, -1.5)', '(2.0, -1.95)']

    ent.setPose( Point(0.0, 0.0), 0.0 )

    bodyPoints= [ str(p) for p in ent.projectedShape().points() ]
    print( f"> return  : {bodyPoints}" )
    assert bodyPoints == ['(-0.43, -0.25)', '(-0.43, 0.25)', '(0.0, 0.5)', '(0.5, 0.0)', '(0.0, -0.5)']

    ent.translate( Point(1.5, -2.0) )
    ent.rotate( 1.67 )

    assert ent.orientation() == 1.67
    assert ent.position().asTuple() == (1.5, -2.0)

    bodyPoints= [ str(p) for p in ent.projectedShape().points() ]
    print( f"> transfom2 : {bodyPoints}" )
    assert bodyPoints == ['(1.79, -2.41)', '(1.29, -2.46)', '(1.0, -2.05)', '(1.45, -1.5)', '(2.0, -1.95)']


def test_fast_entity_body():
    ent= tll.Entity(name="0")

    print(ent)
    tll.draw(ent, "shot-test.svg", 800, 600)
    assert( open("shot-test.svg").read()
        == open("tests/refs/03.01-entity-body-01.svg").read() )

    assert ent.position().asTuple() == (0.0, 0.0)
    assert ent.orientation() == 0.0

    shape= tll.Convex().initArrowTip(0.8)
    shape.rotate(2.2)
    shape.translate( Point(1.0, 0.6) )

    ent.setProjectedShape(shape)
    tll.draw(ent, "shot-test.svg", 800, 600)

    assert shape.round(4).points() == ent.projectedShape().round(4).points()
    
    assert ent.position().round(1).asTuple() == (1.0, 0.6)
    assert ent.orientation() == 0.0

    assert( open("shot-test.svg").read()
        == open("tests/refs/03.01-entity-body-02.svg").read() )

def test_fast_entity_str():
    entity= tll.Entity( 42, tll.Convex().initSquare(1.0), Point(1.0, 2.0) )
    entity.setLocation(12, 6)

    print(entity)
    assert str(entity) == "Entity42 12-6 ⌊(0.5, 1.5), (1.5, 2.5)⌉"

    entity= tll.Entity( 42, tll.Convex().initSquare(1.0) )
    entity.setPosition(1.0, 2.0)
    print(entity)
    assert str(entity) == "Entity42 0-0 ⌊(0.5, 1.5), (1.5, 2.5)⌉"

def test_fast_entity_hacka():
    entity= tll.Entity( 4 ).setPose( Point(1.0, 2.0), 1.5 ).setLocation(3, 42)
    tree= entity.asDataTree()

    assert tree.label() == "Entity"
    assert tree.numberOfDigits() == 3
    assert tree.digits() == [4, 3, 42]
    assert tree.digit(1) == 4
    assert tree.digit(2) == 3
    assert tree.digit(3) == 42
    assert tree.numberOfValues() == 3
    assert tree.values() == [1.0, 2.0, 1.5]
    assert tree.value(1) == 1.0
    assert tree.value(2) == 2.0
    assert tree.value(3) == 1.5
    assert tree.numberOfChildren() == 1
    assert tree.children() == [ entity.referenceShape().asDataTree() ]

    entity2= tll.Entity().fromDataTree(tree)
    tree2= entity2.asDataTree()

    print(tree)
    print("vs")
    print(tree2)
    
    assert str(tree2) == str(tree)

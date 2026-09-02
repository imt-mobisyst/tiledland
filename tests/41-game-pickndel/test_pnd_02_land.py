import sys, hacka, tiledland as tll

"""
Test - Pick'n Del Games Class
"""

workdir= __file__.split('/tests/')[0]
sys.path.insert( 1, workdir )

import src.tiledland.game.pickndel as pnd

"""
Test - Land
"""

refMatrix= [
    [00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
    [00, -1, 00, 00, 00, -1, 00, -1, -1, 00],
    [00, 00, 00, -1, 00, 00, 00, -1, 00, 00],
    [00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
    [00, -1, 00, 00, 00, -1, 00, -1, -1, -1],
    [00, -1, 00, -1, 00, 00, 00, -1, -1, -1],
    [00, 00, 00, 00, 00, -1, 00, -1, -1, -1]
]

"""
    [ 1,  2,  3,   ,  4,  5,  6,  7,  8,  9],
    [10,   , 11, 12, 13,   , 14,   ,   , 15],
    [16, 17, 18,   , 19, 20, 21,   , 22, 23],
    [24, 25, 26,   , 27, 28, 29, 30, 31, 32],
    [33,   , 34, 35, 36,   , 37,   ,   ,   ],
    [38,   , 39,   , 40, 41, 42,   ,   ,   ],
    [43, 44, 45, 46, 47,   , 48,   ,   ,   ]
"""

def test_pnd_land():
    model= pnd.Land( "Cool-Land" )
    assert model.name() == "Cool-Land"

    model.initTabletop( tll.Tabletop().initGrid( refMatrix, 0.9, 0.1 ) )

    pablo= tll.createArtistPNG("shot-test.png", 800, 600)
    pablo.fitBox( model.tabletop().box(), 10 )

    model.tabletop().renderOn(pablo)
    pablo.flip()

    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/41.pickndel-map-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    bob= model.popSimpleActor( tll.Agent(), 1 )

    assert bob == 1
    
    assert model.popActorBody(bob, 25).selector() == (25, 1)
    assert model.popActorBody(bob, 7).selector()  == (7, 1)
    assert model.popActorBody(bob, 44).selector() == (44, 1)

    model.tabletop().renderOn(pablo)
    pablo.flip()

    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/41.pickndel-map-02.png", mode='rb' ).read()
    assert( shotFile == refsFile )

def test_pnd_graph():
    # Game MoveIt:
    land= pnd.Land( "Testland", tll.Tabletop().initGrid( refMatrix, 0.9, 0.1 ) )
    model= land.tabletop()

    print( f">>> {model.neighbours(11)}" )

    assert model.adjacencies(11) == [3, 12, 18]
    assert model.directions(11) == [(0.0, 1.0), (1.0, 0.0), (0.0, -1.0)]
    assert model.clockDirections(11) == [12, 3, 6]

    print( model.neighbours(11) )

    assert model.neighbours(11) == [(3, (0.0, 1.0), 12), (12, (1.0, 0.0), 3), (18,  (0.0, -1.0), 6)]
    
    assert model.completeClock(11) == [11,
                             11, 11, 12, 11, 11, 18,
                             11, 11, 11, 11, 11,  3 ]
    
    assert model.clockPosition(11, 0) == 11
    assert model.clockPosition(11, 12) == 3
    assert model.clockPosition(11, 6) == 18
    assert model.clockPosition(11, 3) == 12
    assert model.clockPosition(11, 9) == 11

def test_pnd_withCarrier():
    # Game MoveIt:
    land= pnd.Land( "Testland", tll.Tabletop().initGrid( refMatrix, 0.9, 0.1 ), numberOfActors=2 )
    tabletop= land.tabletop()

    assert land.popSimpleActor(tll.Agent(), 1)  == 1
    assert land.popActorBody(1, 25).selector() == (25, 1)
    assert land.popSimpleActor(tll.Agent(), 7)  == 2
    assert land.popActorBody(2, 44).selector() == (44, 1)
    
    tll.draw( land.tabletop(), "shot-test.png", 800, 600 )

    print(land.body(1)) 
    assert str( land.body(1) ) == '1:A-1 1-1 ⌊(-0.26, 5.7), (0.3, 6.3)⌉ |0, 0|'

    assert [ e.group() for e in tabletop.tile(1).entities() ] == [1]
    assert str(tabletop.entity(1, 1)) == '1:A-1 1-1 ⌊(-0.26, 5.7), (0.3, 6.3)⌉ |0, 0|'
    assert str(tabletop.entity(1)) == '1:A-1 1-1 ⌊(-0.26, 5.7), (0.3, 6.3)⌉ |0, 0|'

    assert [ e.group() for e in tabletop.tile(2).entities() ] == []
    assert [ e.group() for e in tabletop.tile(7).entities() ] == [2]
    assert [ e.group() for e in tabletop.tile(12).entities() ] == []
    assert [ e.group() for e in tabletop.tile(25).entities() ] == [1]
    assert [ e.group() for e in tabletop.tile(44).entities() ] == [2]
    
    bodyIdentifiers= [
        (b.location(), b.group()) 
        for b in land.allBodies()
    ]

    print( bodyIdentifiers )
    assert bodyIdentifiers == [ (1, 1), (25, 1), (7, 2), (44, 2)]

    #moveEntity

    assert land.move( 11, 12 ) == 11
    assert land.move( 1, 6 ) == 10

    #assert model.entityTiles(1) == [10, 25]
    #assert model.entityTiles(2) == [7, 44]

    assert str( land.tile(10).entity() ) == 'Carrier-1.1 ⌊(-0.18, 4.82), (0.18, 5.18)⌉ |0, 0|'

    assert land.clockBearing(44) == [9, 3]

    assert land.move( 44, 12 ) == False
    assert land.move( 44, 3 ) == 45
    assert land.move( 45, 12 ) == 39
    assert land.move( 39,  0 ) == 39
    assert land.move( 39,  3 ) == False
    
    pablo= tll.createArtistPNG("shot-test.png", 800, 600)
    pablo.fitBox( land.box(), 10 )
    
    land.renderOn(pablo)
    pablo.flip()

    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/41.pickndel-map-03.png", mode='rb' ).read()
    assert( shotFile == refsFile )


    assert model.clockposition( 11, 12 ) == 3
    
"""
    [ 1,  2,  3,   ,  4,  5,  6,  7,  8,  9],
    [10,   , 11, 12, 13,   , 14,   ,   , 15],
    [16, 17, 18,   , 19, 20, 21,   , 22, 23],
    [24, 25, 26,   , 27, 28, 29, 30, 31, 32],
    [33,   , 34, 35, 36,   , 37,   ,   ,   ],
    [38,   , 39,   , 40, 41, 42,   ,   ,   ],
    [43, 44, 45, 46, 47,   , 48,   ,   ,   ]
"""

def test_long_pnd_emcomber():
    # Game MoveIt:
    model= pnd.Land( numberOfPlayers=2 )
    model.initGrid( refMatrix, 0.9, 0.1 )

    for i in range(1, 49) :
        assert model.encumber(i) == 0.0

    # Game MoveIt:
    model= pnd.Land( numberOfPlayers=2 )
    encumber= [
        [ 25,  20,  32  ],
        [ 0.6, 0.5, 0.4 ]
    ]
    model.initGrid( refMatrix, 0.9, 0.1, encumber )

    for i in range(1, 49) :
        if i not in encumber[0] :
            assert model.encumber(i) == 0.0
    
    assert model.encumber(20) == 0.5
    assert model.encumber(25) == 0.6
    assert model.encumber(32) == 0.4

    model.tileAppendEntity( 25, Entity(1) )
    assert str( model.tile(25).entity() ) == 'Carrier-1.1 ⌊(0.82, 2.82), (1.18, 3.18)⌉ |0, 0|'

    encumberCount= 0
    for i in range(10000) :
        if model.move(25, 3) == 25 :
            encumberCount+= 1
        model.teleport(26, 25)
    assert round(encumberCount/10000, 1) == 0.6

    model.teleport(25, 20)
    encumberCount= 0
    for i in range(10000) :
        if model.move(20, 6) == 20 :
            encumberCount+= 1
        model.teleport(28, 20)

    assert round(encumberCount/10000, 1) == 0.5

    model.teleport(20, 32)
    assert str( model.tile(32).entity() ) == 'Carrier-1.1 ⌊(8.82, 2.82), (9.18, 3.18)⌉ |0, 0|'
    encumberCount= 0
    for i in range(10000) :
        if model.move(32, 9) == 32 :
            encumberCount+= 1
        model.teleport(31, 32)

    assert round(encumberCount/10000, 1) == 0.4
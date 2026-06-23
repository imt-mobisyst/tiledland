# HackaGames UnitTest - `pytest`
import sys, re, yaml, msgpack
from PIL import Image
sys.path.insert( 1, __file__.split('tests')[0] )

import src.tiledland as tll
from src.tiledland.geometry import Point, Box, Convex, Grid
from src.tiledland import Agent, Tile, Map 

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - G R I D   T O   M A P
# ------------------------------------------------------------------------ #
from src.tiledland.interface import ros

def test_long_gridmap_loadSmallMap():
    gridmap= ros.GridMap().load( "tests/rsc", "small-map.yaml" )
    grid= gridmap.asGrid()

    assert gridmap.resolution() == 0.1

    convexes= grid.makeConvexes(0, 8)
    tll.artist.drawConvexes(convexes)
    assert len(convexes) == 17
    
    map= tll.Map().fromGridConvexes( grid, 2.0, matters=[Grid.STATE_FREE] )

    tll.artist.drawMap(map)

    shotImg= "shot-test.svg"
    pablo= tll.createArtistSVG(shotImg, 800, 600)
    pablo.fit(map)

    tll.artist.drawMap(map)

    map.draw(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-03-small-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    map= tll.Map().fromGridConvexes( grid, 2.0 )

    tll.artist.drawMap(map)
    
    map.draw(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-03-small-02.svg" )
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_long_gridmap_loadLargeMap():
    gridmap= ros.GridMap().load( "tests/rsc", "large-clean-map.yaml" )
    grid= gridmap.asGrid()

    assert gridmap.resolution() == 0.1

    shotImg= "shot-test.svg"
    pablo= tll.createArtistSVG(shotImg, 800, 600)

    map= tll.Map().fromGridConvexes( grid, 2.0, matters=[Grid.STATE_FREE] )

    tll.artist.drawMap(map)

    pablo.fit(map)
    map.draw(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-03-large-01.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    map= tll.Map().fromGridConvexes( grid, 2.0 )
    
    tll.artist.drawMap(map)
    
    pablo.fit(map)
    map.draw(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-03-large-02.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

def test_gridmap_rosGridMap_webots():
    gridmap= Grid()

    # Lecture du fichier binaire
    with open("tests/rsc/webots-grid.mpk", "rb") as f:
        buf = f.read()
        rosOccupGrid= msgpack.unpackb(buf, raw=False)

    width, height= rosOccupGrid['width'], rosOccupGrid['height'] 
    grid= rosOccupGrid['grid']
    
    resolution= rosOccupGrid['resolution']
    pos_x= rosOccupGrid['pos_x']
    pos_y= rosOccupGrid['pos_y']

    assert [width, height, resolution, pos_x, pos_y] == [ 103, 162, 0.05, -1.4355376215141014, -3.1116143188991185 ]
    
    img = Image.new("RGB", (width, height))
    for y in range(height):
        for x in range(width):
            value= grid[y][x]
            if value == 0 :
                img.putpixel( (x, y), (255,255,255) )
            elif value == 100 :
                img.putpixel( (x, y), (0,0,0) )
            else :
                img.putpixel( (x, y), (127,127,127) )

    # Sauvegarde en PNG
    img.save("shot-test.png", format="PNG")

    shotFile= open( "shot-test.png", mode='rb' ).read()
    refsFile= open( "tests/refs/interface-ros-03-webots-01.png", mode='rb' ).read()
    assert( shotFile == refsFile )

    # Test msgpack :

    # Sérialisation -> écriture fichier binaire
    with open("shot-webots-grid.mpk", "wb") as f:
        packed = msgpack.packb(rosOccupGrid, use_bin_type=True)
        f.write(packed)
    print(f"Sérialisé ({len(packed)} octets)")

    # Désérialisation -> lecture fichier binaire
    with open("shot-webots-grid.mpk", "rb") as f:
        buf = f.read()
        dico2 = msgpack.unpackb(buf, raw=False)
    print("Désérialisé :", dico2)

    assert rosOccupGrid == dico2

    gridmap= ros.transformOccupMap( grid, (pos_x, pos_y), resolution )

    assert gridmap.resolution() == 0.05
    assert gridmap.bottomleft().asTuple() == (-1.4355376215141014, -3.1116143188991185)
    assert gridmap.dimention() == (103, 162)

    shotImg= "shot-test.svg"
    pablo= tll.createArtistSVG(shotImg, 800, 600)

    map= tll.Map().fromGridConvexes( gridmap, 2.0, matters=[Grid.STATE_FREE, Grid.STATE_OCCUPIED] )
    pablo.fit(map)
    map.draw(pablo)
    pablo.flip()

    shotFile= open( shotImg ) 
    refsFile= open( "tests/refs/interface-ros-03-webots-map.svg" ) 
    for lineShot, lineRef in zip( shotFile, refsFile ):
        assert( lineShot == lineRef )

    for tile in map.tiles() :
        print( tile )
    
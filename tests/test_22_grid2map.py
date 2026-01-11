# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland.geometry import Float2, Box
from src.tiledland import Shape, Agent, Tile, Scene 

# ------------------------------------------------------------------------ #
#         T E S T   T I L E D L A N D - G R I D   T O   M A P
# ------------------------------------------------------------------------ #
from src.tiledland import rosi

def test_gridmap_cells():
    gridmap= rosi.GridMapStat()
    
    gridmap.setGrid([
        [1.0, 0.5, 0.0, 0.0],
        [0.0, 0.2, 0.9, 0.0],
        [0.0, 0.0, 0.1, 0.0]
    ])

    assert gridmap.dimention() == (4, 3)
    assert gridmap.cell(0, 0) == 0.0
    assert gridmap.cellIsFree(0, 0) 
    assert not gridmap.cellIsOccupied(0, 0)
    assert not gridmap.cellIsUncertain(0, 0) 

    assert not gridmap.cellIsFree(0, 2) 
    assert gridmap.cellIsOccupied(0, 2)
    assert not gridmap.cellIsUncertain(0, 2) 

    assert not gridmap.cellIsFree(1, 2) 
    assert not gridmap.cellIsOccupied(1, 2)
    assert gridmap.cellIsUncertain(1, 2) 

    assert gridmap.cellIsFree(2, 0)
    assert gridmap.cellIsOccupied(2, 1)

    realGridmap= gridmap.asGridMap()
        
    realGridmap.setGrid([
        [1, 2, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ])

def test_gridmap_boxing():
    gridmap= rosi.GridMap()
    
    gridmap.setGrid([
        [0, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0]
    ])

    assert gridmap.box(0, 0) == [0, 0, 1, 1]

    gridmap.setGrid([
        [1, 1, 1, 0],
        [1, 1, 1, 0],
        [0, 0, 1, 0]
    ])
    assert gridmap.box(0, 0) == [0, 0, 2, 1]

    gridmap.setGrid([
        [1, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ])
    assert gridmap.box(0, 0) == [0, 0, 2, 2]

    gridmap.setGrid([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    assert gridmap.box(0, 0) == [0, 0, 4, 3]

    gridmap.setGrid([
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ])
    assert gridmap.box(0, 0) == [0, 0, 2, 3]

    gridmap.setGrid([
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ])
    assert gridmap.box(0, 0) == [0, 0, 2, 3]

def test_gridmap_search():
    gridmap= rosi.GridMap()
    gridmap.setGrid([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    assert gridmap.search() == (0, 0)
    assert gridmap.search(1) == False

    gridmap= rosi.GridMap()
    gridmap.setGrid([
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [2, 2, 0, 0]
    ])
    assert gridmap.search() == (2, 0)
    assert gridmap.search(1) == (2, 1)

def test_gridmap_allbox():
    gridmap= rosi.GridMap()
    gridmap.setGrid([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    boxes= gridmap.makeBoxes()
    assert boxes == [ [0, 0, 4, 3] ]

    print( "Grid" )
    for line in gridmap.grid() :
        print(line)

    assert gridmap.grid() == [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    gridmap.setGrid([
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ])
    boxes= gridmap.makeBoxes()

    print( "Boxes" )
    for box in boxes :
        print(box)

    assert boxes == [
        [0, 0, 2, 3],
        [2, 0, 4, 1],
        [3, 1, 4, 3],
        [2, 2, 3, 3]
    ]

    print( "Grid" )
    for line in gridmap.grid() :
        print(line)

    assert gridmap.grid() == [
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ]

    gridmap.setGrid([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    ])
    boxes= gridmap.makeBoxes()

    print( "Boxes" )
    for box in boxes :
        print(box)

    assert boxes == [
        [0, 0, 8, 7],
        [8, 0, 19, 2],
        [21, 0, 24, 7],
        [10, 2, 19, 4],
        [14, 4, 19, 7],
        [8, 5, 14, 7],
        [19, 5, 21, 7]
    ]

def test_gridmap_asRectangles():
    gridmap= rosi.GridMap()
    gridmap.setGrid([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    ])
    r= gridmap.boxToRectangle( [14, 4, 19, 7] )
    assert r == []
    rectancles= gridmap.makeRectangles()
    assert rectancles == [
        []
    ]
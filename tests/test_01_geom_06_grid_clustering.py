# HackaGames UnitTest - `pytest`
import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland.geometry import Point, Grid

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def test_grid_clusterIterations():
    grid= Grid()
    
    grid.initialize([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    ])

    assert grid.height() == 7
    assert grid.width() == 24

    means= grid.clusterInit(0, 4)
    means.round(2)
    assert means.size() == 3
    assert means.asTuples() == [(4, 4.07), (12, 4.07), (20, 4.07)]

    assert grid.localPointToCoordinate( Point(4, 4.07) ) == (4, 4)
    assert grid.localPointToCoordinate( Point(4, 4.57) ) == (4, 5)

    assert grid.cell(4, 4) == 0
    assert grid.searchClosest(0, 4, 4) == (4, 4, 0)

    assert grid.cell(20, 4) == 1
    assert grid.searchClosest(0, 20, 4) == (19, 4, 1)

    marks, means= grid.clusterIterate(0, means, 4)
    assert marks.dimention() == (24, 7)

    print(marks)
    assert "\n"+ str(marks) == """
Grid 24x7
| 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3
| 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3
| 1 1 1 1 1 1 1 1 · · · · · · 2 3 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 · · 2 2 2 2 2 3 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 · · 2 2 2 2 2 3 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 3 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 3 3 3 3 · · 3 3 3
0 -----------------------------------------------"""
    print(  means.copy().round(2).asTuples() )
    assert means.copy().round(2).asTuples() == [(4.83, 4.17), (12.66, 3.6), (19.91, 4.19)]

    # Iteration 1 :
    marks, newMeans= grid.clusterIterate(0, means, 4)
    dists= [ round(p.distance(np), 2) for p, np in zip( means.points(), newMeans.points() ) ]
    means= newMeans

    print(marks)
    assert "\n"+ str(marks) == """
Grid 24x7
| 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3
| 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3
| 1 1 1 1 1 1 1 1 · · · · · · 2 2 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 · · 2 2 2 2 2 2 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 · · 2 2 2 2 2 2 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 3 3 3 · · 3 3 3
0 -----------------------------------------------"""
    print(  means.copy().round(2).asTuples() )
    print( dists )
    assert means.copy().round(2).asTuples() == [(4.83, 4.17), (13.21, 3.67), (20.5, 4.22)]

    # Iteration 2 :
    marks, newMeans= grid.clusterIterate(0, means, 4)
    dists= [ round(p.distance(np), 2) for p, np in zip( means.points(), newMeans.points() ) ]
    means= newMeans

    print(marks)
    assert "\n"+ str(marks) == """
Grid 24x7
| 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3
| 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3
| 1 1 1 1 1 1 1 1 · · · · · · 2 2 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 · · 2 2 2 2 2 2 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 · · 2 2 2 2 2 2 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 3 3 · · 3 3 3
0 -----------------------------------------------"""
    print(  means.copy().round(2).asTuples() )
    print( dists )
    assert means.copy().round(2).asTuples() == [(4.83, 4.17), (13.21, 3.67), (20.5, 4.22)]


    # Iteration 3 :
    marks, newMeans= grid.clusterIterate(0, means, 4)
    dists= [ p.distance(np) for p, np in zip( means.points(), newMeans.points() ) ]
    means= newMeans

    print(marks)
    assert "\n"+ str(marks) == """
Grid 24x7
| 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3
| 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3
| 1 1 1 1 1 1 1 1 · · · · · · 2 2 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 · · 2 2 2 2 2 2 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 · · 2 2 2 2 2 2 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 3 3 · · 3 3 3
0 -----------------------------------------------"""
    print(  means.copy().round(2).asTuples() )
    print( dists )
    assert means.copy().round(2).asTuples() == [(4.83, 4.17), (13.21, 3.67), (20.5, 4.22)]
    assert min(dists) < 0.001

def test_grid_clustering():
    grid= Grid()
    
    grid.initialize([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    ])

    marks, means= grid.clustering(0, 4)
    print(  means.copy().round(2).asTuples() )
    assert means.copy().round(2).asTuples() == [(4.83, 4.17), (13.21, 3.67), (20.5, 4.22)]

    # Iteration Test :
    marks, newMeans= grid.clusterIterate(0, means, 4)
    dists= [ p.distance(np) for p, np in zip( means.points(), newMeans.points() ) ]
    assert means.asTuples() == newMeans.asTuples()

    print(marks)
    assert "\n"+ str(marks) == """
Grid 24x7
| 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3
| 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3
| 1 1 1 1 1 1 1 1 · · · · · · 2 2 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 · · 2 2 2 2 2 2 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 · · 2 2 2 2 2 2 3 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 3 3 · · 3 3 3
| 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 3 3 · · 3 3 3
0 -----------------------------------------------"""
    print(  means.copy().round(2).asTuples() )
    print( dists )
    assert means.copy().round(2).asTuples() == [(4.83, 4.17), (13.21, 3.67), (20.5, 4.22)]
    assert min(dists) < 0.001


def test_grid_clusterSmall():
    grid= Grid()
    
    grid.initialize([
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    ])

    assert grid.height() == 7
    assert grid.width() == 24

    means= grid.clusterInit(0, 4)
    means.round(2)
    assert means.size() == 3
    assert means.asTuples() == [(4, 4.07), (12, 4.07), (20, 4.07)]

    marks, means= grid.clusterIterate(0, means, 4)

    print(marks)
    assert "\n"+ str(marks) == """
Grid 24x7
| · · · · · · · · 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2
| · · · · · · · · 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2
| · · · · · · · · · · · · · · 1 2 2 2 2 · · 2 2 2
| · · · · · · · · · · 1 1 1 1 1 2 2 2 2 · · 2 2 2
| · · · · · · · · · · 1 1 1 1 1 2 2 2 2 · · 2 2 2
| · · · · · · · · 1 1 1 1 1 1 1 2 2 2 2 · · 2 2 2
| · · · · · · · · 1 1 1 1 1 1 1 2 2 2 2 · · 2 2 2
0 -----------------------------------------------"""

    marks, means= grid.clustering(0, 4)
    print(marks)
    assert "\n"+ str(marks) == """
Grid 24x7
| · · · · · · · · 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2
| · · · · · · · · 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2
| · · · · · · · · · · · · · · 1 1 2 2 2 · · 2 2 2
| · · · · · · · · · · 1 1 1 1 1 1 2 2 2 · · 2 2 2
| · · · · · · · · · · 1 1 1 1 1 1 2 2 2 · · 2 2 2
| · · · · · · · · 1 1 1 1 1 1 1 1 2 2 2 · · 2 2 2
| · · · · · · · · 1 1 1 1 1 1 1 1 2 2 2 · · 2 2 2
0 -----------------------------------------------"""



def test_grid_clusterLot():
    grid= Grid()
    
    grid.initialize([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    ])

    marks, means= grid.clustering(0, 2)

    print(marks)

    means.round(2)
    assert means.size() == 11
    print( means.asTuples() )
    assert means.asTuples() == [
        (2.36, 2.29), (6.5, 2.29), (10.83, 2.17),
        (14.4, 2.4), (18.09, 2.36), (23.07, 2.86),
        (3.17, 5.67), (7.79, 6.0), (12.5, 6.5),
        (16.5, 5.71), (21.36, 6.29)
    ]

    assert "\n"+ str(marks) == """
Grid 24x7
| 7 7 7 7 7 8 8 8 8 8 9 9 9 9 A A A A B B B B B B
| 7 7 7 7 7 8 8 8 8 8 9 9 9 9 A A A A B B B B B B
| 7 7 7 7 7 8 8 8 · · · · · · A A A A B · · B B 6
| 1 1 7 7 7 2 2 8 · · 3 3 4 4 4 A A 5 5 · · 6 6 6
| 1 1 1 1 2 2 2 2 · · 3 3 4 4 4 4 5 5 5 · · 6 6 6
| 1 1 1 1 2 2 2 2 3 3 3 3 4 4 4 4 5 5 5 · · 6 6 6
| 1 1 1 1 2 2 2 2 3 3 3 3 4 4 4 4 5 5 5 · · 6 6 6
0 -----------------------------------------------"""

def test_grid_clusterHulls():
    grid= Grid( position= Point(10.0, 5.0), resolution=0.1 )
    
    grid.initialize([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    ])

    marks, means= grid.clustering(0, 2)
    
    assert marks.position().asTuple() == (10.0, 5.0)
    assert marks.resolution() == 0.1

    marks.filter(0, -1)
    shapes= marks.makeHulls()

    assert False
    
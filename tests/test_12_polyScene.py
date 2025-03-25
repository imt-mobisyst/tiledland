import sys
sys.path.insert( 1, __file__.split('tests')[0] )

from src.tiledland.geometry import Float2, Box
from src.tiledland import Shape, Agent, Tile, Scene 

from src import tiledland as tll

# ------------------------------------------------------------------------ #
#         T E S T   H A C K A G A M E S - C O M P O N E N T
# ------------------------------------------------------------------------ #

def draw(scene, filePath= "output.png"):
    pablo= tll.Artist().initializePNG( filePath )
    
    pablo.drawFrameGrid()
    pablo.drawFrameAxes()

    pablo.drawSceneNetwork( scene )
    pablo.drawSceneTiles( scene )

    pablo.flip()

def test_scene_incremental():
    scene= Scene()
    
    assert type(scene) == Scene
    assert scene.size() == 0
    assert scene.box() == Box()

    index= scene.append( Tile( shape= Shape() ) )
    assert index == 1
    assert scene.size() == 1

    print( scene.tile(1) )
    assert scene.tile(1).position().asTuple() == (0.0, 0.0)
    assert scene.tile(1).envelope() == []

    index= scene.append( Tile( shape= Shape() ) )
    assert index == 2
    assert scene.size() == 2

def test_scene_clockNeighboring():
    scene= Scene()
    tileShape= Shape().fromZipped(
        [(-1.0, 0.0), (0.0, 1.5), (1.0, 0.0), (0.0, -1.5) ]
    )
    scene.append( Tile( shape=tileShape, matter= 1 ) )

    draw(scene)

    assert scene.neighbours(1) == []

    index= scene.append( Tile( shape= tileShape, position=Float2(1.5, 2), matter= 2 ) )
    scene.connect( 1, index )    
    assert scene.neighbours(1) == [(2, 1)]
    draw(scene)

    index= scene.append( Tile( shape= tileShape, position=Float2(-1.5, 2), matter= 2 ) )
    scene.connect( 1, index )    
    draw(scene)
    assert scene.neighbours(1) == [(2, 1), (3, 11)]

    index= scene.append( Tile( shape= tileShape, position=Float2(1.5, -2), matter= 2 ) )
    scene.connect( 1, index )    
    index= scene.append( Tile( shape= tileShape, position=Float2(-1.5, -2), matter= 2 ) )
    scene.connect( 1, index )    
    draw(scene)
    assert scene.neighbours(1) == [(2, 1), (3, 11), (4, 5), (5, 7)]

    assert scene.tile(1).adjacencies() == [2, 3, 4, 5]
    assert scene.edges() == [(1, 2), (1, 3), (1, 4), (1, 5)]

def test_Scene_initLine():
    scene= Scene().initializeLine(3)
    assert scene.tile(1).id() == 1
    assert scene.tile(2).id() == 2
    assert scene.tile(3).id() == 3
    assert scene.tiles() == [ scene.tile(1), scene.tile(2), scene.tile(3) ]
    assert scene.edges() == []

    assert scene.tile(1).position().asTuple() == (0.0, 0.0)
    assert scene.tile(1).envelope() == [(-0.45, 0.45), (0.45, 0.45), (0.45, -0.45), (-0.45, -0.45) ]

    assert scene.tile(2).position().asTuple() == (1.0, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in scene.tile(2).envelope() ]
    assert env == [(0.55, 0.45), (1.45, 0.45), (1.45, -0.45), (0.55, -0.45)]

    assert scene.tile(3).position().asTuple() == (2.0, 0.0)
    env= [ (round(x, 2), round(y, 2)) for x, y in scene.tile(3).envelope() ]
    assert env == [(1.55, 0.45), (2.45, 0.45), (2.45, -0.45), (1.55, -0.45)]
    
def test_Scene_construction():
    scene= Scene().initializeLine(3)
    assert scene.tile(1).adjacencies() == []
    assert scene.tile(2).adjacencies() == []
    assert scene.tile(3).adjacencies() == []
    scene.connect(1, 2)
    scene.connect(1, 3)
    scene.connect(2, 2)
    scene.connect(2, 1)
    scene.connect(3, 1)
    scene.connect(3, 2)
    scene.connect(3, 3)
    assert scene.tile(1).adjacencies() == [2, 3]
    assert scene.tile(2).adjacencies() == [1, 2]
    assert scene.tile(3).adjacencies() == [1, 2, 3]
    assert scene.edges() == [ (1, 2), (1, 3), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3) ]
    idScene= id(scene)
    scene.initializeLine(3)
    scene.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    print(f">>> {scene.edges()}")
    assert( idScene == id(scene) )
    assert scene.edges() == [ (1, 1), (1, 3), (2, 1), (2, 2), (3, 2) ]

def test_Scene_str():
    scene= Scene().initializeLine(3)
    scene.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )
    scene.tile(2).append( Agent(1) )

    print( f">>> {scene}." )

    assert "\n"+str(scene)+"\n" == """
Scene:
- Tile-1 ⌊(-0.45, -0.45), (0.45, 0.45)⌉ adjs[1, 3] agents(0)
- Tile-2 ⌊(0.55, -0.45), (1.45, 0.45)⌉ adjs[1, 2] agents(1)
  - Agent-1 ⌊(-0.2, -0.2), (0.2, 0.2)⌉
- Tile-3 ⌊(1.55, -0.45), (2.45, 0.45)⌉ adjs[2] agents(0)
"""

def test_Scene_pod():
    scene= Scene().initializeLine(4)
    scene.connectAll( [ [1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4],
                       [3, 1], [3, 2], [4, 1], [4, 2]
                        ] )

    scene.tile(1).position().set( 5.0, 3.0 )
    scene.tile(2).position().set( 5.0, 15.0 )
    scene.tile(3).position().set( 1.0, 9.0 )
    scene.tile(4).position().set( 9.0, 9.0 )

    print(f">>>\n{scene}")
    assert '\n'+ str(scene) +'\n' == """
Scene:
- Tile-1 ⌊(4.55, 2.55), (5.45, 3.45)⌉ adjs[2, 3, 4] agents(0)
- Tile-2 ⌊(4.55, 14.55), (5.45, 15.45)⌉ adjs[1, 3, 4] agents(0)
- Tile-3 ⌊(0.55, 8.55), (1.45, 9.45)⌉ adjs[1, 2] agents(0)
- Tile-4 ⌊(8.55, 8.55), (9.45, 9.45)⌉ adjs[1, 2] agents(0)
"""

def test_Scene_box():
    scene= Scene()
    assert scene.box() == Box( [Float2(0.0, 0.0)] )

    scene= Scene().initializeLine(4)
    print( scene.box() )
    assert scene.box().asZip() == [(-0.45, -0.45), (3.45, 0.45)]
    
    scene.initializeGrid( [[0, 1], [0, -1]] )
    print( scene.box() )
    assert scene.box().asZip() == [(-0.5, -0.5), (1.6, 1.6)]

def test_Scene_podable():
    scene= Scene().initializeLine(3)
    scene.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )

    pod= scene.asPod()

    assert pod.numberOfWords() == 1
    assert pod.words() == ["Scene"]
    assert pod.word() == "Scene"

    assert pod.numberOfIntegers() == 0
    assert pod.integers() == []
    
    assert pod.numberOfValues() == 0
    assert pod.values() == []
    
    assert pod.numberOfChildren() == 3
    assert pod.children() == [ t.asPod() for t in scene.tiles() ]

def test_Scene_podcopy():
    scene= Scene().initializeLine(3)
    scene.connectAll( [ [1, 3], [1, 1], [2, 2], [2, 1], [3, 2], [3, 2] ] )

    assert scene.edges() == [(1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]

    assert '\n'+ str(scene) +'\n' == """
Scene:
- Tile-1 ⌊(-0.45, -0.45), (0.45, 0.45)⌉ adjs[1, 3] agents(0)
- Tile-2 ⌊(0.55, -0.45), (1.45, 0.45)⌉ adjs[1, 2] agents(0)
- Tile-3 ⌊(1.55, -0.45), (2.45, 0.45)⌉ adjs[2] agents(0)
"""

    print("Go for the copying...")
    sceneBis= scene.podCopy()
    scene.connect(3, 1)

    assert type(scene) == type(sceneBis)
    assert sceneBis.size() == 3

    print(f">>>\n{sceneBis}")
    assert '\n'+ str(sceneBis) +'\n' == """
Scene:
- Tile-1 ⌊(-0.45, -0.45), (0.45, 0.45)⌉ adjs[1, 3] agents(0)
- Tile-2 ⌊(0.55, -0.45), (1.45, 0.45)⌉ adjs[1, 2] agents(0)
- Tile-3 ⌊(1.55, -0.45), (2.45, 0.45)⌉ adjs[2] agents(0)
"""

    assert sceneBis.edges() == [(1, 1), (1, 3), (2, 1), (2, 2), (3, 2)]

def test_Scene_connection():
    scene= Scene().initializeLine(3)
    scene.connect(1, 2)
    scene.connect(2, 2)
    scene.connect(2, 3)
    scene.connect(3, 2)
    print( f"---\n{scene}.")
    assert str(scene) == """Scene:
- Tile-1 ⌊(-0.45, -0.45), (0.45, 0.45)⌉ adjs[2] agents(0)
- Tile-2 ⌊(0.55, -0.45), (1.45, 0.45)⌉ adjs[2, 3] agents(0)
- Tile-3 ⌊(1.55, -0.45), (2.45, 0.45)⌉ adjs[2] agents(0)"""

    assert scene.tile(1).adjacencies() == [2]
    assert scene.tile(2).adjacencies() == [2, 3]
    assert scene.tile(3).adjacencies() == [2]
    
    assert scene.isEdge(1, 2)
    assert scene.isEdge(2, 2)
    assert scene.isEdge(3, 2)
    assert not scene.isEdge(2, 1)
    assert not scene.isEdge(1, 3)
    assert not scene.isEdge(3, 1)

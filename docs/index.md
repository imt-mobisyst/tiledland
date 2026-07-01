# TiledLand: A Polygon-based Simulation Engine.

This project is a `Python` package oriented toward multi-agent simulation reling on a convex polygonal objects.
The main idea is to model a plan world (the land) as a collection of convex-polygons cells (the tiles).
Then, the land is mainly composed of a map - interconnected tiles - and agents distributed inside it.

To notice that, _TiledLand_ is more a sandbox project to test approaches than an optimized, ready-to-use and well documented toolbox.

- On github: [imt-mobisyst/tiledland](https://github.com/imt-mobisyst/tiledland)
- On PyPip: [projct tiledland](https://pypi.org/project/tiledland/)

## Not what are you looking for ?

You can look at concurrent/complementary projects:

- [Box2d](https://box2d.org) a 2d physics game engine
- [pygame](https://www.pygame.org) a python-based game engine
- [raylib](https://www.raylib.com/) a simple cross language game engine
- [shapely](https://pypi.org/project/shapely) to manipulate in python geometric objects in the cartesian plane (based on [GEOS](https://libgeos.org/))
- [cgal](https://www.cgal.org) another Computational Geometry Algorithms Library (c++)


## Install

The project and its dependencies can be installed with _pip_ tool.

```sh
pip install tiledland
```

For information, _TiledLand_ relies on [pyyaml](https://pypi.org/project/PyYAML) to read _yaml_ configuration files, on [hacka](https://github.com/ktorz-net/hacka-py) for distributed game programming and on  [Cairo](https://pypi.org/project/pycairo/) library for _PNG_ image rendering. 

You can also install _TiledLand_ from source: [github.com - tiledland](https://github.com/imt-mobisyst/tiledland).


## Get started

Then, as an exemple, the following code will generate a grid-land with 3 square agents in position _9_, _14_ and _26_.
The land is then rendered as a _png_ graphic.

```python
#!env python3
import tiledland as tll

# Create a new TiledMap as a grid:
land= tll.Map()
land.initGrid([
	[0, 1, 1, -1, 0, 0, 0, 0], # -1 : means no cell at this location
	[5, -1, 0, 2, 0, -1, 5, 0], # 0 - n : give the group identifier
	[0, 0, 0, -1, 0, 1, 1, 0], # of the cell to create.
	[0, 4, 0, -1, 0, 2, 1, 6],
	[-1, -1, 0, 0, 0, -1, -1, -1]
])

# Agent 1
agent= land.popAgentOn(9)

# Agent 2
agent= land.popAgentOn(26)
agent.setMatter(13)

# Agent 3
agent= land.popAgentOn(14)
agent.setMatter(15)

# Create an artist to render this map:
dali= tll.createArtistPNG( "shot-demo.png", 800, 600 )
dali.fitBox( land.box() )
land.renderOn(pablo)
dali.flip() # Uptate and save the support and return to a blanc page.

print( f"You can open now the './{dali.support().filePath()}' file." )
```

## Structure

_TiledLand_ is structured with several sub-modules, each one dedicated to a functionality.

- _geometry_ :  Polygon-based objects and the map definition.
- _artist_ : for rendering geometry objects
- _main_ : Build on top of `geometry` and `artist`, the main tiledland elements: `entities`, `tiles`, `maps` and `agents`
- _games_ : few example games.
- _interfaces_ : offering tools making _TiledLand_ easely integrable with external solutions like ROS2, Web IHM (with Remi). To notice that _TiledLand_ is not dependant to the python packages targeted with _interface_ components.

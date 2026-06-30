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
its relies [pyyaml](https://pypi.org/project/PyYAML) to read _yaml_ configuration files and [hacka](https://github.com/ktorz-net/hacka-py) for distributed game programming.
The project requires also [Cairo](https://pypi.org/project/pycairo/) library for _PNG_ image rendering example. 
This dependency is not mandatory, but all example and demonstration generating or reading _PNG_ image will fail. 
Only _SVG_ rendering is available by default.

```sh
pip install pycairo tiledland
```

You can also install _TiledLand_ from source on [github.com - tiledland](https://github.com/imt-mobisyst/tiledland).


## Getting started

Then, as an exemple, the following code will generate a grid-land with 3 square agents in position _9_, _14_ and _26_.
The land is then rendered as a _png_ graphic.

```python
#!env python3
import tiledland as tll

# Create a new TiledMap as a grid:
map= tll.Map()
map.initGrid([
	[0, 1, 1, -1, 0, 0, 0, 0], # -1 : means no cell at this location
	[5, -1, 0, 2, 0, -1, 5, 0], # 0 - n : give the group identifier
	[0, 0, 0, -1, 0, 1, 1, 0], # of the cell to create.
	[0, 4, 0, -1, 0, 2, 1, 6],
	[-1, -1, 0, 0, 0, -1, -1, -1]
])

# Agent 1
agent= map.popAgentOn(9)

# Agent 2
agent= map.popAgentOn(26)
agent.setMatter(13)

# Agent 3
agent= map.popAgentOn(14)
agent.setMatter(15)

# Create an artist to render this map:
pablo= tll.createArtistPNG( "shot-demo.png", 800, 600 )
pablo.fitBox( map.box() )
map.renderOn(pablo)
pablo.flip() # Uptate the support and return to a blanc page.

print( f"You can open now the './{pablo.support().filePath()}' file." )
```

## Structure

The _Python_ module _TiledLand_ is structured with several sub-modules, each one dedicated to a functionality.

- _geometry_ :  Polygon-based objects and the map definition.
- _mas_ : multi-agent def.
- _artist_ : for rendering stuff
- _games_ : 
- _interfaces_ offering program interface tool for external solutions like ROS2, Web IHM (with Remi).

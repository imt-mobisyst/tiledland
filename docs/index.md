# TiledLand: A Polygon-Based Simulation Engine.

This project is a `Python` package oriented toward multi-agent simulation relying on convex polygonal objects.
The main idea is to model a planar world (the land) as a collection of convex-polygon cells (the tiles).
Then, the land is mainly composed of a tabletop - interconnected tiles - and agents distributed inside it.

To notice that, _TiledLand_ is more a sandbox project to test approaches than an optimized, ready-to-use and well documented toolbox.

- On github: [imt-mobisyst/tiledland](https://github.com/imt-mobisyst/tiledland)
- On PyPip: [project tiledland](https://pypi.org/project/tiledland/)

## Not what are you looking for ?

You can look at concurrent/complementary projects:

- [box2d](https://box2d.org) - 2d physics game engine (in _C_ language but with a lot of binds)
- [pygame](https://www.pygame.org) - python-based game engine
- [raylib](https://www.raylib.com/) - simple cross language game engine
- [shapely](https://pypi.org/project/shapely) to manipulate, in python geometric objects in the Cartesian plane (based on [GEOS](https://libgeos.org/)).
- [cgal](https://www.cgal.org) another Computational Geometry Algorithms Library (c++)


## Install

The project and its dependencies can be installed with the _pip_ tool.

```sh
pip install tiledland
```

For information, _TiledLand_ relies on [pyyaml](https://pypi.org/project/PyYAML) to read _yaml_ configuration files, on [hacka](https://github.com/ktorz-net/hacka-py) for distributed game programming, and on  [Cairo](https://pypi.org/project/pycairo/) library for _PNG_ image rendering. 

You can also install _TiledLand_ from source: [github.com - tiledland](https://github.com/imt-mobisyst/tiledland).


## Get started

Then, as an example, the following code will generate a grid-tabletop with several entities.
The tabletop is then rendered as a _png_ graphic.

```python
import tiledland as tll

# Create a new land (a tiled tabletop and entities inside it) :
tabletop= tll.Tabletop()
tabletop.initGrid([
	[0, 1, 1, -1, 0, 0, 0, 0], # -1 : means no cell at this selector
	[5, -1, 0, 2, 0, -1, 5, 0], # 0 - n : give the group identifier
	[0, 0, 0, -1, 0, 1, 1, 0], # of the cell to create.
	[0, 4, 0, -1, 0, 2, 1, 6],
	[-1, -1, 0, 0, 0, -1, -1, -1]
])

# Define a small shape for our entities...
shape= tll.Convex().initRegular( 0.4, 5 )

# Add several entities associate to different groups...
tabletop.tileAppendEntity( 8, tll.Entity(1, shape, name="A1") )
tabletop.tileAppendEntity( 16, tll.Entity(1, shape, name="A2") )
tabletop.tileAppendEntity( 4, tll.Entity(2, shape, name="B1") )
tabletop.tileAppendEntity( 19, tll.Entity(2, shape, name="B2") )
tabletop.tileAppendEntity( 24, tll.Entity(3, shape, name="C1") )
tabletop.tileAppendEntity( 28, tll.Entity(3, shape, name="C2") )

# Create an artist to render this tabletop:
tll.draw( tabletop, "shot-demo.png", 800, 600 )

print( f"You can open now the './shot-demo.png' file." )
```

## Structure

_TiledLand_ is structured with several sub-modules, each one dedicated to a functionality.

- _geometry_ :  Polygon-based objects and the tabletop definition.
- _artist_ : for rendering geometry objects
- _core_ : Build on top of `geometry` and `artist`, it defines the main tiledland elements: `entities`, `tiles` and `tabletops`.
- _agent system_ : A upper-layer built on top of _TiledLand core_  elements with `land` and `agents` for agent-based modeling.
- _games_ : few example games.
- _interfaces_ : offering tools making _TiledLand_ easily integrable with external solutions like ROS2, Web IHM (with Remi). To notice that _TiledLand_ is not dependent on the Python packages targeted with _interface_ components.

# TiledLand: Polygon-based simulation engine.

The main idea is to model a plan world as a collection of convex-polygons objects.
The world is mainly composed of an environnement and items and agents distributed inside it with convex-based interconnected tiles for the environment.

Its is more a sandbox project to test approaches than an optimized, ready-to-use and well documented toolbox.

The project relies on [Cairo](https://pypi.org/project/pycairo/) library for rendering example, [pyyaml](https://pypi.org/project/PyYAML) to read _yaml_ configuration files and [hacka](https://github.com/ktorz-net/hacka-py) for distributed game programming.

## Not what are you looking for ?

You can look at concurrent/complementary projects:

- [Box2d](https://box2d.org) a 2d physics game engine
- [pygame](https://www.pygame.org) a python-based game engine
- [raylib](https://www.raylib.com/) a simple cross language game engine
- [shapely](https://pypi.org/project/shapely) to manipulate in python geometric objects in the cartesian plane (based on [GEOS](https://libgeos.org/))
- [cgal](https://www.cgal.org) another Computational Geometry Algorithms Library (c++)


## Install

The _Tiled-Land_ project can be installed with _pip_.

```sh
pip install tiledland
```


For in-dev version, refer to github repository : [imt-mobisyst/tiled-land](https://www.github.com/imt-mobisyst/tiled-land).


### Get started

The `demo` directory include simple examples for _TiledLand_.
Most of the demonstrations generate a scene, rendered in a `shot-demo.png` file.

In _VisualStudio Code_ terminal for instance:

```shell
cd demo
python3 01-grid-scene.py 
code shot-demo.png
python3 02-hexa-world.py
python3 03-loading-gridmap.py 
```

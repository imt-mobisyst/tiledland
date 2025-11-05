# TiledLand: Polygon-based simulation engine.

The main idea is to model a plan world as a polygon-based interconnected tiles for the environment and to add mobile objects inside.
This project targets a map of an environment as a 2.5 dimensions model structured as a collection of linked cells with convex borders.

Its is more a sandbox project to test approaches than an optimized, ready-to-use and well documented toolbox.

The project relies on [Cairo](https://pypi.org/project/pycairo/) and [pygame](https://pypi.org/project/pygame/) library for rendering example and [shapely](https://pypi.org/project/shapely), itself based on [geos](https://pypi.org/project/pygame/) for geometric primitives.

Its composed of two module: `agent based modeling` and `Convex polygone based geometry`.


## Not what you looking for ?

- [Box2d]
- [pygame]
- [RayLib]


## Install

The _Tiled-Land_ project can be installed with `pip`.
TODO: Add shapely dependency to `pyproject.toml`, 
Also the project is based on pytest for testing.

```sh
git clone git@github.com:imt-mobisyst/tiled-land.git
cd tiled-land
pytest
pip install .
```

### Get started

The `example-scene.py` file provides a simple example for _TiledLand_. 
The command  `python3 example-scene.py` should instantiate a scene from a grid environment and 3 agents.
The Scene is then rendered into `/shot-example.svg` file.
 
### Bitmap rendering

Rendering can be  generated thanks to  of `cairo`, by switching from a _SVG_ artist initialization to a _PNG_ one. 

```sh
pip install pycairo
```

To notice that `cairo` rendering is compatible with `pygame` to create a complete interactive game based on _TiledLand_.

### Web rendering

streamlit

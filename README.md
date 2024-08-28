# Tiled-Land: Agent based simulation on polygon-based cells map.

This project targets a map of an environement as a 2.5 dimention model structured as a collection of linked cells with convex borders.

Its is more a sandbox project to test ideas than an optimized, ready-to-use and well documented toolbox.
Its composed of two module: `tiledMap` and `tiledLand`.

The project relies on [Cairo](https://pypi.org/project/pycairo/) and [pygame](https://pypi.org/project/pygame/) librairy for rendering example and [shapely](https://pypi.org/project/shapely), itself based on [geos](https://pypi.org/project/pygame/) for geometric primitives.


To-do: 

- Explore [igraph](https://python.igraph.org) possibilities.

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

### Pygame/Cairo Examples

PolyMap need to be installed on your computer using `pip`.

```sh
pip install cairo pygame
```

The 'example-simpleSim.py' file provides a simple example for _MarauBotMap_. The command `python3 example-xx-xxx.py` should instanciate a simulation and open it on a windows.
 

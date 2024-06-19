# Tiled-Map: polygon-based cells map

This project targets a map of an environement as a 2.5 dimention model structured as a collection of linked cells with convex borders.
The project aims to be as independant as possible, but it relies on [Cairo](https://pypi.org/project/pycairo/)and [pygame](https://pypi.org/project/pygame/) librairy for rendering example.

Project Components:

- pyPolyMap: a pure _Python_ implementation of PolyMap
- PolyMap: a _C_ implementation of PolyMap coopled to a python wrap.

Convex-Map is not what you looking for ? Take a look at: 

- [shapely](https://pypi.org/project/shapely/).

## Install

The _PolyMap_ is mainly independant, but its construction is based on `cmake` and `python3-pip`.
Also the project is based on pytest for testing.

```sh
git clone git@github.com:imt-mobisyst/poly-map.git
cd poly-map
pytest
pip install .
```

### Cairo Examples

PolyMap need to be installed on your computer using `pip`.

```sh
pip install cairo pygame
```

The 'example-simpleSim.py' file provides a simple example for _MarauBotMap_. The command `python3 example-simpleSim.py` should instanciate a simulation and open it on a windows.
 
- packaging: https://packaging.python.org/en/latest/

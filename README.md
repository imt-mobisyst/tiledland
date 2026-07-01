# TiledLand: Polygon-based simulation engine.

The main idea is to model a plan world as a collection of convex-polygons objects.
The world is mainly composed of an environnement and items and agents distributed inside it with convex-based interconnected tiles for the environment.

Its is more a sandbox project to test approaches than an optimized, ready-to-use and well documented toolbox.

The project relies on [Cairo](https://pypi.org/project/pycairo/) library for rendering example ; [pyyaml](https://pypi.org/project/PyYAML) and [msgpack](https://msgpack.org/) to read/write respectivelly configuration and serialized-object files ; [hacka](https://github.com/ktorz-net/hacka-py) for distributed game programming.

- On github: [imt-mobisyst/tiledland](https://github.com/imt-mobisyst/tiledland)
- On PyPip: [projct tiledland](https://pypi.org/project/tiledland/)


### Get started

The _TiledLand_ project can be installed with _pip_ (directly or after cloning).
To notice that, the project is based on _pytest_ for testing.

```sh
git clone git@github.com:imt-mobisyst/tiled-land.git
cd tiled-land
pytest -k "not long" # to shunt time consuming tests
pip install .
```

The `demo` directory include simple examples for _TiledLand_.
Most of the demonstrations generate a map, rendered in a `shot-demo.png` file.

In VisualStudio Code terminal for instance:

```shell
cd demo
python3 01-grid-map.py 
code shot-demo.png
python3 02-hexa-world.py
python3 03-loading-gridmap.py 
```

## Documentation
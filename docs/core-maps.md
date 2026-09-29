# Maps and Tile Conversion

## Building from a Grid

```python
from tiledland import Grid, Point, Tabletop, draw

grille = Grid([[0, 0, 1], [0, 0, 1]], Point(0.0, 0.0), 0.5)
plateau = Tabletop().fromGridConvexes(
    grille, tileSize=1.0, minSizeRatio=0.1, pixelValues=[0]
)
assert plateau.numberOfTiles() > 0
draw(plateau, "carte.svg", 600, 400)
```

`pixelValues=[0]` here limits the conversion to free space. `fromGridConvexes()` produces polygons and then connects nearby tiles. `fromGridRectangles()` is another path: it builds rectangles and then attempts mergers.

## Importing ROS-type Maps

Explicitly import the module:

```python
from tiledland.interface.ros import loadGridMap
from tiledland import Tabletop

grille = loadGridMap("tests/rsc", "small-map.yaml")
plateau = Tabletop().fromGridConvexes(grille, tileSize=1.0, pixelValues=[0])
assert plateau.numberOfTiles() > 0
```

Run this example from the root of the repository, where the test map is located. The loader reads a YAML file and the referenced PNG image using PyYAML and Cairo; it does not start any ROS node.

The YAML must provide `image`, `resolution`, `origin`, `occupied_thresh`, `free_thresh`, `mode`, and `negate`. The implementation requires `mode: trinary`, `negate: 0` or `false`, and an image decoded by Cairo in RGB24 format. Only the first two components of `origin` are used: map rotation is not applied.

PNGs with transparency or a different format may be rejected. Free, occupied, and unknown states are calculated from the file's thresholds. The import does not guarantee perfect geometric coverage or constant performance on large maps.

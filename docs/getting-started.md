# Installation and First Scene

## Prerequisites

The project declares Python **3.10 or later**. Its dependencies are `hacka`, `pyyaml`, `pycairo`, and `msgpack`. Cairo is notably used to produce PNG images; its installation may require system libraries depending on the machine.

From the root of the repository:

```sh
python -m pip install tiledland
```

The editable installation allows using `import tiledland` while working on the repository sources. Files are written in the directory from which the program is launched.

## Creating and Drawing a World

Save this program as `premiere_scene.py`, then execute it with `python premiere_scene.py`:

```python
import tiledland as tild

plateau = tild.Tabletop().initGrid([
    [0, 0, 1],
    [0, -1, 0],
])
robot = tild.Entity(
    group=1,
    shape=tild.Convex().initArrowTip(0.6),
    name="Robot",
)
plateau.tileAppendEntity(1, robot)
tild.quickDraw(plateau, "", "premiere-scene.svg", 800, 500)
assert plateau.numberOfTiles() == 5
assert robot.enclave() == 1
print("Scene saved to premiere-scene.svg")
```

Open the SVG in a browser. Positive or zero values in the matrix designate the groups of the tiles; `-1` leaves an empty spot. A group is a category that notably influences the color: it does not automatically constitute a movement prohibition rule.

## Moving an Object

```python
import tiledland as tild

plateau = tild.Tabletop().initLine(3)
robot = plateau.tileAppendEntity(1, tild.Entity(name="Robot"))
plateau.tileMoveEntity(robot.enclave(), robot.index(), 2)
assert robot.selector() == (2, 1)
tild.quickDraw(plateau, "", "deplacement.svg", 800, 300)
```

This operation replaces the entity at the center of the target tile. It does not control the existence of an edge between the two tiles. To respect the graph, verify `plateau.isEdge(depart, arrivee)` before movement.

Continue with [tabletop concepts](core-tabletop.md) and [rendering](core-rendering.md).

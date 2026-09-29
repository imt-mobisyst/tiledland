# Tiles and Tabletops

`Tile` inherits from `Entity` and adds a list of neighbors and a collection of entities. `Tabletop` gathers these tiles and provides operations on their graph and content.

## Building the Tabletop

| Method | Usage |
| --- | --- |
| `initLine(size, tileSize=1.0, separation=0.1, connect=True)` | Line of tiles |
| `initGrid(matrix, tileSize=1.0, separation=0.1, connect=True)` | Rectangular grid |
| `initHexa(matrix, tileSize=1.0, separation=0.1, connect=True)` | Hexagonal grid |
| `fromShapes(shapes, group=0)` | Tabletop built from polygons |
| `createTile(shape, group=0)` | Adding a tile |

Initialization methods replace existing tiles. `fromShapes()` does not automatically build connections.

```python
from tiledland import Tabletop

plateau = Tabletop().initHexa([[0, 0], [0, -1]])
assert plateau.numberOfTiles() == 3
for tuile in plateau.tiles():
    print(tuile.index(), tuile.adjacencies())
```

## Connections

`connect(a, b)` creates a directed connection from `a` to `b`. To allow both directions, also add `connect(b, a)`.

```python
from tiledland import Tabletop

plateau = Tabletop().initLine(2, connect=False)
plateau.connect(1, 2)
assert plateau.isEdge(1, 2)
assert not plateau.isEdge(2, 1)
plateau.connect(2, 1)
```

`adjacencies(i)` provides neighbor identifiers; `edges()` provides source-target pairs. `neighbours(i)` adds a relative movement and a clock direction for each neighbor.

`connectAllClose(distance)` connects tiles whose geometric distance is strictly lower than the threshold. This search examines all pairs; its cost increases rapidly with the number of tiles.

## Tile Content

`tileAppendEntity(i, objet)` adds and centers the object. `entity(i, j)` finds the entity with index `j` in tile `i`. `tileRemoveEntity(i, j)` returns the removed entity or `None` if it does not exist. `tileMoveEntity(i, j, cible)` removes and then adds the object at the destination.

Indices start at **1**. Validate identifiers before accessing collections: accessors are not all validity controls and a null index may select the last element through Python indexing.

`tiles()`, `entities()`, and `adjacencies()` expose modifiable internal collections. Modifying them directly can desynchronize counters or selectors; prefer model operations.

## Clock Directions

Constants `Action.DIR_N`, `DIR_E`, `DIR_S`, and `DIR_W` are respectively 12, 3, 6, and 9. Intermediate directions divide the turn into twelve sectors. This referencing does not replace path planning. Oriented movements still have limits described in the [dedicated page](limitations.md).

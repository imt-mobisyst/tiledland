# Serialization and Copies

Model objects offer a `hacka.DataTree` representation. It allows transmitting a structure and reconstructing objects; it is not by itself a versioned save policy.

## Entity Round-trip

```python
from tiledland import Entity

source = Entity(group=2, name="Robot").setPosition(1.0, 2.0)
arbre = source.asDataTree()
restauree = Entity().fromDataTree(arbre)
assert restauree.name() == "Robot"
assert restauree.position().asTuple() == (1.0, 2.0)
assert restauree.group() == 2
```

The entity notably encodes its name, group, selector, pose, and reference shape. A customized brush is not serialized as such; do not assume that the appearance will be strictly preserved.

## Copying a Tabletop Without Entities

```python
from tiledland import Tabletop

source = Tabletop().initLine(2)
copie = source.dataTreeCopy()
assert copie.numberOfTiles() == 2
assert copie.numberOfEntities() == 0
copie.clear()
assert source.numberOfTiles() == 2
```

Restoring a tabletop containing entities currently fails: `Tile.setIndex()` calls a missing `Entity.setArea()` method. This example is therefore limited to tabletops without entities.

`Tabletop` exposes `dataTreeCopy()` via `AbsEntity`, and not `copy()`. Subclasses and their additional attributes are not automatically preserved: define an explicit format before serializing custom business objects. Defects in managing shared shapes make a check for data independence necessary for advanced uses.

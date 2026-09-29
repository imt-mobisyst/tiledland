# Entities and Transformations

An `Entity` has a name, a group, a reference shape, a position, an orientation, and a selector `(location, index)`.

## Two Shape Representations

The **reference shape** describes the object in its local coordinate system. The **projected shape** represents this shape after rotation and translation in the world. Pose transformations rebuild the projection from the reference.

```python
import math
from tiledland import Entity, Convex, Point

objet = Entity(shape=Convex().initSquare(0.8), name="Caisse")
objet.setPose(Point(2.0, 1.0), math.pi / 2)
assert objet.position().asTuple() == (2.0, 1.0)
objet.translate(Point(1.0, 0.0))
assert objet.position().asTuple() == (3.0, 1.0)
```

Angles are expressed in radians. `setOrientation(angle)` replaces the orientation; `rotate(angle)` adds a rotation. `setPosition(x, y)` replaces the position; `translate(vecteur)` adds a displacement.

## Identity and Ownership

`name()` is a label. `group()` is a numerical category. `location()` indicates the tile and `index()` the position of the object in its collection; objects added to the tabletop receive indices starting from 1.

These indices can change when an entity is removed. Re-read `selector()` after a movement instead of keeping an old index.

## Copying and Modifying a Shape

`copy()` creates a new entity with its own position and projection, but notably shares the reference shape and the brush. This is not a deep copy of all attributes. Avoid modifying a shared reference; assign a new shape to the copy:

```python
from tiledland import Entity, Convex

original = Entity(name="Original")
copie = original.copy()
copie.setReferenceShape(Convex().initSquare(0.4))
copie.setPosition(2.0, 0.0)
assert original.position().asTuple() == (0.0, 0.0)
```

For an arrow, use `setReferenceShape(Convex().initArrowTip(...))`. The `setShapeArrowTip()` method is currently defective. `setProjectedShape()` also has a problem when a previous orientation is non-zero: see the [limits](limitations.md).

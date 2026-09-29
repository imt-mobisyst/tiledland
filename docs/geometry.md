# Geometry

Geometric classes use 2D coordinates and angles in radians. The choice of distance unit belongs to the application; maintain the same unit for shapes, positions, and map resolutions.

## Points and Segments

```python
from tiledland import Point, Line

origine = Point(0.0, 0.0)
point = Point(3.0, 4.0)
assert origine.distance(point) == 5.0
segment = Line(origine, point)
assert segment.lenght() == 5.0
```

The name `lenght()` corresponds to the current spelling of the API. `Point` specifically provides `distance`, `dotProduct`, `crossProduct`, `translate`, `rotate`, and `copy`. Several operations modify the object in place; copy a point before transforming data that must be preserved.

## Convex Polygons

```python
from tiledland import Convex, Point

carre = Convex().initSquare(2.0)
assert carre.isIncludingPoint(Point(0.0, 0.0))
copie = carre.copy()
copie.translate(Point(3.0, 0.0))
assert not copie.isIncludingPoint(Point(0.0, 0.0))
```

`initSquare`, `initRegular`, and `initArrowTip` provide predefined shapes. `box()` calculates a bounding box; `isIncludingPoint()` tests membership; `isColliding()` and `distance()` compare two polygons. The algorithms expect convex polygons: do not assume that any concave shape will be interpreted correctly.

`points()` exposes the internal points. A direct mutation of a shape used as a reference by multiple entities can affect multiple objects.

## Grids

`Grid(values, bottomleft, resolution)` represents a discrete matrix associated with an origin and a resolution. Predefined states are `STATE_FREE`, `STATE_OCCUPIED`, and `STATE_UNKWON` (API spelling).

```python
from tiledland import Grid, Point

grille = Grid([[0, 1], [0, 0]], Point(0.0, 0.0), 0.5)
assert grille.dimention() == (2, 2)
assert grille.cell(2, 2) == 1
```

`cell(x, y)` uses indices starting from **1**, unlike the underlying Python lists. The vertical axis is counted from the bottom: the first row of the matrix corresponds to the highest `y` value.

`makeRectangles()` and `makeConvexes()` extract regions to build a tabletop. Their size parameters should not be assumed to be a size in meters without verification: conversion operations also use the resolution. The recommended path is that of the [maps](maps.md) page.

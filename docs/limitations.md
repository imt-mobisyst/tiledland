# Known Limits

This page describes the state of the examined code, not fixed features. Regression tests added to the project make several defects visible.

| Area | Current Limit | Practice to Adopt |
| --- | --- | --- |
| `Agent.decide()` | Returns `None` after state execution | Explicitly use `runStateProcessus()` |
| `Agent.copy()` | Fails with a `Tabletop`; incorrect assignment of the tabletop copy | Explicitly build a new agent |
| `Agent.perceive()` / `HackaAgent` | Features not implemented | Define perception and transport in the application |
| `Entity.setShapeArrowTip()` | Incorrect call to the shape constructor | Use `setReferenceShape(Convex().initArrowTip(...))` |
| `Entity.setOutline()` | Does not reset the effective orientation attribute | Prefer a reference shape and `setPose()` |
| Default `Land` bank | List and models shared between instances | Provide a new list of new entities |
| Copies and collections | Some internal data remains shared or directly modifiable | Explicitly define object ownership |

## Tabletop Restoration

Verification of examples revealed that `dataTreeCopy()` fails on a tabletop containing an entity: `Tile.setIndex()` calls `Entity.setArea()`, a missing method. The serialization example is therefore limited to a tabletop without entities.

## Movements and Orientations

A reading of `tileOrientEntity()` and `tileRotateEntity()` shows that they select the first entity of the tile instead of passing the requested index. `tileClockMoveEntity()` also performs a rotation call with the target identifier after the movement. These points must be corrected and tested before relying on these methods in scenes with multiple bodies. Tutorials use direct movement and transformations on the entity itself.

## Scale and Robustness

`connectAllClose()` compares pairs of tiles, which represents a quadratic cost in the number of tiles even before the cost of polygonal distances. Measure times on target maps before sizing an experiment.

Several validations rely on `assert`. The Python `-O` option disables them; it can even remove calls placed in an assertion, such as a tile creation in `fromGridRectangles()`. Do not use this mode for this version.

## Tests

During the initial audit, before the local correction of `perceivedBody()`, the suite with the new tests showed: **137 successes, 8 failures, 7 tests excluded** by the `not long` filter. The failures are defects expected by the audit but remain true failures: they are not masked by `xfail`. This historical balance is not the result of the corrected version. `perceivedBody()` now returns the body in the local code; rerun the suite to obtain an updated balance.

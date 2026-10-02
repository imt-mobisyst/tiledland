# Practical Reference

This reference selects the operations necessary for tutorials. It does not replace an exhaustive description of all experimental methods.

| Class | Methods | Result / Usage |
| --- | --- | --- |
| `Entity` | `setPosition(x, y)`, `setOrientation(angle)`, `setPose(point, angle)` | Modify pose |
| `Entity` | `position()`, `orientation()`, `selector()` | Read position, angle, and ownership |
| `Entity` | `referenceShape()`, `projectedShape()`, `box()` | Local and world geometry |
| `Entity` | `copy()` | Copy with some shared attributes |
| `Mobile` | Inherits `Entity` | Specialized entity for mobile objects |
| `Tabletop` | `initLine`, `initGrid`, `initHexa`, `fromShapes` | Build the world |
| `Tabletop` | `tile(i)`, `entity(i, j=1)` | Access with indices starting from 1 |
| `Tabletop` | `numberOfTiles()`, `numberOfEntities()` | Count elements |
| `Tabletop` | `connect(a, b)`, `isEdge(a, b)`, `adjacencies(i)` | Directed graph |
| `Tabletop` | `tileAppendEntity(i, obj)` | Returns the added entity |
| `Tabletop` | `tileMoveEntity(i, j, cible)` | Returns the moved entity or `None` |
| `Tabletop` | `dataTreeCopy()` | Reconstruction via DataTree, currently limited to tabletops without entities |
| `Land` | `appendActor(agent, tileIds, bodyIds)` | Returns the actor identifier |
| `Land` | `body(actorId, iBody=1)`, `actor(actorId)` | Find an actor or its body |
| `Agent` | `setStateProcessus(method)`, `runStateProcessus()` | Define and execute a state |
| `Action` | `identifier()`, `attributes()`, `attribute(i=0)` | Read an intention |
| `Artist` | `fit(obj)`, `flip()` | Framing and finalization |

## Conventions to Remember

- Tiles and actor bodies are indexed starting from 1; action attributes starting from 0.
- Angles use radians; clock directions use distinct integers.
- A construction method often returns `self`, but not always. Verify before chaining operations not illustrated in tutorials.
- Several accessors return internal objects, not copies.
- Methods identified as defective are detailed in [known limits](limitations.md).

# Land and Actors

A `Land` associates a `Tabletop`, a bank of entity models, and a list of actors. An `Actor` links an agent to several bodies. Bodies are the entities actually placed on the tabletop.

## Adding an Actor

```python
from tiledland import Land, Tabletop, Entity, Convex, Agent, draw

land = Land(
    tabletop=Tabletop().initLine(3),
    bankOfEntities=[Entity(shape=Convex().initArrowTip(0.6), name="Robot")],
)
acteur_id = land.appendActor(Agent(), tileIds=[1], bodyIds=[0])
corps = land.body(acteur_id)
assert corps.location() == 1
land.tabletop().tileMoveEntity(corps.location(), corps.index(), 2)
assert corps.location() == 2
draw(land.tabletop(), "acteur.svg", 800, 300)
```

`bodyIds` selects models from the bank; `tileIds` selects placement tiles. Both lists must have the same length: the implementation iterates through them using `zip` and therefore ignores excess elements.

## Identifiers

Actor 0 is reserved during initialization. Added actors receive identifiers starting from 1. In an actor, `body(1)` designates the first body. Bank models use indexing starting from 0 and `bankEntity()` applies a modulo to the bank size: provide a non-empty bank and explicit identifiers.

`popSimpleActor(agent, tuile)` creates an actor with one body. `popActorBody(acteur, tuile, entityNum)` adds a body to an existing actor. `actor(id).bodies()` allows enumerating its bodies.

## Limits

The presence of an agent in `Land` does not trigger any automatic perception-decision-action loop. The application must orchestrate the simulation flow. Provide an explicit bank as in the example: the default parameter currently shares objects between instances.

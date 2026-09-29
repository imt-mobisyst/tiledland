# Agents and Decisions

The `Agent` class offers a minimal state machine. A state is a function that receives the agent and produces an `Action`. `Action` preserves an identifier and attributes: `WAIT=0`, `MOVE=1`, `ROTATE=2`.

## Executing a State

```python
from tiledland import Agent, Action

def aller_est(agent):
    agent.setStateProcessus(Agent.stateInfinitWait)
    return Action(Action.MOVE, Action.DIR_E)

agent = Agent(state=aller_est)
action = agent.runStateProcessus()
assert action.identifier() == Action.MOVE
assert action.attribute(0) == Action.DIR_E
assert agent.runStateProcessus().identifier() == Action.WAIT
```

The default agent starts in `stateInitialize`, which produces a wait and then selects `stateInfinitWait`. `setStateProcessus()` accepts a function or a bound method.

## Application Responsibility

An action is an intention; it does not modify the world. The application must read its identifier, determine a destination, verify the rules, and then modify the tabletop. An explicit loop for movement on a graph can be:

```python
from tiledland import Agent, Action, Entity, Tabletop

plateau = Tabletop().initLine(2)
corps = plateau.tileAppendEntity(1, Entity())
agent = Agent(state=lambda agent: Action(Action.MOVE, 2))
action = agent.runStateProcessus()
if action.identifier() == Action.MOVE:
    destination = action.attribute(0)  # Local convention: tile identifier.
    if plateau.isEdge(corps.location(), destination):
        plateau.tileMoveEntity(corps.location(), corps.index(), destination)
assert corps.location() == 2
```

This example explicitly chooses a tile as an action attribute; the previous example chose a direction. `Action` does not impose a schema: fix a convention in each simulation.

## Current State

`perceive()` does not yet update perception. `decide()` currently returns `None`, even when a state produces an action; therefore, examples use `runStateProcessus()`. `perceivedBody()` returns the body in the corrected local code. Copying an agent with a tabletop still has defects. `HackaAgent` is an empty class, without an operational distributed transport. See [tests and limits](limitations.md).

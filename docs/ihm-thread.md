# Execution and Concurrency

The model uses lists and mutable objects. It provides no built-in locking, no thread-safety guarantee, and no simulation scheduler.

## Sequential Loop

For a first simulation, evolve the world in an explicit order: prepare an observation, request a decision, validate the action, modify the world, then produce the render. The choice of simultaneous or sequential actions belongs to the application; it can modify the result of an experiment.

Generic agents are still incomplete. Use the operational methods described in the [agents](as-agent.md) page and define transition rules in the application.

## Adding a Concurrent Interface

One possible organization consists of entrusting all modifications to a single thread and passing commands to it via a queue. The rendering thread must read a consistent state: protect reading and writing or prepare an independent display representation.

A simple copy of `Entity` does not guarantee the absence of shared shapes or brushes. Do not consider `copy()` as complete isolation between threads.

## Reproducibility

Fix the seeds of random generators used by the application, record scenario parameters, and preserve the execution order of actions. The engine does not do this automatically.

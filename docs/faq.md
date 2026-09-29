# Frequently Asked Questions

## Why does the installation fail on Cairo?

`pycairo` is a declared dependency. Depending on the environment, its compilation requires Cairo system components and Python development headers. Examine the installation message and prepare these components using the platform's tools.

SVG support does not import Cairo in its main rendering path, but the standard project installation always requires `pycairo`, and ROS map imports use Cairo. There is currently no official "SVG only" installation option.

## Why does an old example call a missing method?

Some demonstrations use `popAgentOn`, `setAgentFactory`, or `setMatter`, which are absent from the current core API. Start with the [getting started guide](getting-started.md), whose Python blocks have been executed on local sources.

## Why does my object change position after being added?

`tileAppendEntity()` places the entity at the center of the tile. For a different position within the area, define the pose after adding. Geometry and logical ownership are not automatically resynchronized when moving an entity directly.

## Does a group represent an obstacle?

Not by itself. The group is a category used notably for appearance. Accessibility, collision, and movement rules must be established by the scenario.

## Why does `decide()` not return any action?

This is a current defect. The [agents](as-agent.md) page shows the direct use of `runStateProcessus()`.

## How to launch the documentation?

From the repository: `python -m mkdocs serve`. Dependencies and static construction are described in the [contribution guide](development.md).

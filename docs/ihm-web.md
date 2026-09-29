# Web Interface

The repository contains experiments with Streamlit and Remi in `demo/ihm-streamlit/` and `demo/ihm-remi/`. These dependencies are not part of the main declared dependencies and old simulation examples may target an earlier API.

## First Integration

The simplest path consists of producing an SVG with `draw()`, then displaying it in the chosen interface. Buttons or other commands update the model before requesting a new render.

An application must distinguish the world state, commands, and display. If multiple users connect, explicitly decide if they share a simulation or each have their own `Land`.

## Exploring Demonstrations

The file `demo/ihm-remi/01-basic.py` illustrates a web window with a button and a label, without a simulation engine. Demonstration folders constitute integration paths; they are not all covered by the example validation of this documentation.

The module `artist/webapp.py` is currently empty: it does not provide a ready-to-launch application server. TiledLand also does not define an action network protocol, session management, or authentication.

## Updating the Display

Start with an update after each command. Then add a refresh frequency if the experience requires it, avoiding redraws of an unchanged scene. Concurrency issues are addressed in [execution and concurrency](ihm-thread.md).

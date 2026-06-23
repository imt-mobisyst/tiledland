# Board V0.1:


## Get Tiledland from Hackagames.tiled

- [x] Initialize with hackagames.tiled
- [x] Initialize artist rendering
- [x] New Structure: core (Map, Tiles and Agents), geometry and artist
- [x] HackaGame compatible
- [ ] asDico() and fromDico() morphing (via Pop)

## Map, Tiles and Agents :

- [x] Agents: Position, clock-position and Convex
- [x] Map as collection of: group's Agents, structured on Tiles
- [x] Tiles as collection of: Agents
- [x] Abstraction on Map: Agents could be anything...
- [x] Grid and Hexa-grid based map initilization.


## Rendering :

- [x] Artist + support architectur.
- [x] SVG Support.
- [x] PNG Support with Cairo.
- [ ] Add Texure to Convex...
- [ ] Projection simple : (vertical ratio)
- [ ] Free Projection : (rotation + translation)


## Manipulate the map : 

- [ ] Basic Map manipulation: doSomething ... doTeleportOn(tile, agent, group).
- [ ] Be topological: Clockdir manipulation.


## Documentation :

- [ ] Presentation of _Core_ components (game)
- [ ] Presentation of _Geometry_ submodule
- [ ] Developpers expectation: (template from Convex + class structure + tests)


## HackaGames - SocNav

Social complient navigation.


## HackaGames - Pick'n Del

Pick-up and Delivery with hiden random congestion.

- [x] Carrier from Agents and World from Map.
- [x] Mission on market place (origin destination)
- [x] Hacka compatible GameMaster
- [x] First players and first of documentation.
- [x] Uncertainty with encumbered tiles
- [ ] Dedicated documentation on ktorz-net.github.io
- [ ] Handle seral carriers
- [ ] MultiPlayer version
- [ ] Multiple mission and - carrier capacity
- [ ] encumbered value function of population/directions


# HackaGames - Move-It

Based on MultiPath solving problem.

- [ ] Mobile from Agent and World from Map.
- [ ] Mission: position to reach, where something need to be done.
- [ ] NPC and Collision between mobiles.
- [ ] Hacka compatible GameMaster.
- [ ] Dedicated documentation on ktorz-net.github.io
- [ ] Handle seral Mobiles.
- [ ] MultiPlayer version.


## Web Rendering :

- [ ] Identifing a tool _flask_, _streamlit_, _django_, _dash by plotly_
- [ ] Visualize map (Static/Dynamic)
- [ ] Add a monitor/control panel
- [ ] Make the map clickable...


## Simple, but strong plan geometry

- [ ] Decide lib-based or independant ([shapely](https://pypi.org/project/shapely), itself based on [geos](https://pypi.org/project/pygame/) for geometric primitives)
- [ ] Convex min/max radius, and collision.
- [ ] Convex update with a radius.
- [ ] Segment automatic tag.
- [ ] get a tiles from a position (in max radius, and closest)
- [ ] Agents: update position and Convex function (auto-centering)
- [ ] Map: Generation from graphs, Voroi, gabriel, ....
- [ ] Convex: Collisions


## Explorations

- [ ] decide lib-based or independant - (Explore [igraph](https://python.igraph.org) possibilities)
- [ ] Agent Based Model (or not ?): Step engine, also in a way compatible to hackagames

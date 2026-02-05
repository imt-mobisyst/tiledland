# Board:

**-- Board V0.1 --**

## Get Tiledland from Hackagames.tiled

- [x] Initialize with hackagames.tiled
- [x] Initialize artist rendering
- [x] New Structure: core (Scene, Tiles and Agents), geometry and artist
- [x] HackaGame compatible
- [ ] asDico() and fromDico() morphing (via Pod)


## Simple, but strong plan geometry

- [x] Convex obj. min/max radius, and collision
- [x] Scene: Gridmap to Tiled Scenes 
- [x] Fast position requestest : add a grid canvas to Scene get a tiles from a position (getTile at, closest, inRadius ...)
- [ ] Agents: update position and Convex function (auto-centering) (Agent: `perceive(Obs)`, `decide()` and Environement/Game/Scene: `forward(agent, action)` (But on Hacka?) )
- [ ] Scene: Generation from Voroi, gabriel, ....


## Web IHM - Rendering

- [x] Artist + support architectur.
- [x] SVG Support.
- [x] PNG Support with Cairo.
- [ ] Visualize map (Static/Dynamic)
- [ ] Add a monitor/control panel
- [ ] Make the map clickable...
- [ ] Validate the choise of remi
- [ ] Add Texure to Convex...
- [ ] Projection simple : (vertical ratio)
- [ ] Free Projection : (rotation + translation)


## Scene, Tiles and Agents :

- [x] Agents: Position, clock-position and Convex
- [x] Scene as collection of: group's Agents, structured on Tiles
- [x] Tiles as collection of: Agents
- [x] Abstraction on Scene: Agents could be anything...
- [x] Grid and Hexa-grid based scene initilization.
- [ ] Basic Scene manipulation: doSomething ... doTeleportOn(tile, agent, group).
- [ ] Be topological: Clockdir manipulation.


## HackaGames - Pick'n Del

Multi-Modal (Dynamic) Pick-up and Delivery with hiden random congestion.

- [x] Carrier from Agents and World from Scene.
- [x] Mission on market place (origin destination)
- [x] Hacka compatible GameMaster
- [x] First players and first of documentation.
- [x] Uncertainty with encumbered tiles
- [ ] Dedicated documentation on ktorz-net.github.io
- [ ] Handle seral carriers
- [ ] MultiPlayer version
- [ ] Multiple mission and - carrier capacity
- [ ] encumbered value function of population/directions


**-- Board V0.2 --**


## Go efficient :

- [ ] Migrate geometry module on a _C_ library (`lib42deg` - a lib. for 2D Euclidean Geom.)
- [ ] Encapsulate Convex in Modif object (ie. one or several join convexes)
- [ ] Migrade Scene geometry function into a Texture dedicated object.



## HackaGames - Multi-Bot Delivery

Simple multiple robots game focused on 1 piece at a time delivery.


## HackaGames - Robot SocNav

Social complient navigation.

- [ ] Human simulation model


## Documentation :

- [ ] Presentation of _Core_ components
- [ ] Presentation of _Hacka Distribution_
- [ ] Presentation of _Geometry_ submodule
- [ ] Presentation of _Rendering_ solution
- [ ] Tuto _Web IHM_
- [ ] Tuto _pygame IHM_
- [ ] Tuto _create a game_
- [ ] Developpers expectation: (template from Convex + class structure + tests)




# HackaGames - Move-It

Based on MultiPath solving problem.

- [ ] Mobile from Agent and World from Scene.
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


## Explorations

- [ ] decide lib-based or independant - (Explore [igraph](https://python.igraph.org) possibilities)
- [ ] Agent Based Model (or not ?): Step engine, also in a way compatible to hackagames

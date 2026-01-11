# Board V0.1:


## Get Tiledland from Hackagames.tiled

- [x] Initialize with hackagames.tiled
- [x] Initialize artist rendering
- [x] New Structure: core (Scene, Tiles and Agents), geometry and artist
- [x] HackaGame compatible
- [ ] asDico() and fromDico() morphing (via Pod)


## Simple, but strong plan geometry

- [ ] Decide: self-dependant (create `lib42deg`) or lib-based 1: [shapely](https://pypi.org/project/shapely), itself based on [geos](https://pypi.org/project/pygame/) for geometric primitives ; 2: [box2d](https://box2d.org/)
- [ ] Shape min/max radius, and collision.
- [ ] Shape update with a radius.
- [ ] Segment automatic tag.
- [ ] get a tiles from a position (in max radius, and closest)
- [ ] Agents: update position and Shape function (auto-centering) (Agent: `perceive(Obs)`, `decide()` and Environement/Game/Scene: `forward(agent, action)` (But on Hacka?) )
- [ ] Scene: Based on a graph
- [ ] Scene: Graphs <-> Gridmap
- [ ] Scene: Generation from Voroi, gabriel, ....


## Scene, Tiles and Agents :

- [x] Agents: Position, clock-position and Shape
- [x] Scene as collection of: group's Agents, structured on Tiles
- [x] Tiles as collection of: Agents
- [x] Abstraction on Scene: Agents could be anything...
- [x] Grid and Hexa-grid based scene initilization.
- [ ] Basic Scene manipulation: doSomething ... doTeleportOn(tile, agent, group).
- [ ] Be topological: Clockdir manipulation.


## HackaGames - Multi-Bot Delivery

Simple multiple robots game focused on 1 piece at a time delivery.


## HackaGames - Robot SocNav

Social complient navigation.

- [ ] Human simulation model


## Web IHM - Rendering

- [x] Artist + support architectur.
- [x] SVG Support.
- [x] PNG Support with Cairo.
- [ ] Visualize map (Static/Dynamic)
- [ ] Add a monitor/control panel
- [ ] Make the map clickable...
- [ ] Validate the choise of remi
- [ ] Add Texure to Shape...
- [ ] Projection simple : (vertical ratio)
- [ ] Free Projection : (rotation + translation)


## Documentation :

- [ ] Presentation of _Core_ components
- [ ] Presentation of _Hacka Distribution_
- [ ] Presentation of _Geometry_ submodule
- [ ] Presentation of _Rendering_ solution
- [ ] Tuto _Web IHM_
- [ ] Tuto _pygame IHM_
- [ ] Tuto _create a game_
- [ ] Developpers expectation: (template from Shape + class structure + tests)



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

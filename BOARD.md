# Board:

**-- Board V0.1.x --**

## Geometrical Toolbox :

- [x] Basic point, line, and polygon objects in 2D frame.
- [x] Simple rectangular boxing.
- [x] Main Convex object to represent a convex polygon.
- [x] Convex obj. min/max radius, and collision
- [x] Map: Gridmap to Tiled Maps


## Artist Rendering :


## Tiledland Core Structures

the core component of TiledLand refere to the `Tiles` composing a `Map` and comtainning `Entities`.

- [x] `Entity` the root class with group, id and shape, a convex delimitation of the element.
- [x] The `Entity` shape is defined with a reference shape (static, centered on (0.0, 0.0 and potentially shared between several entities) and a projected shape (a transformed reference shape in the map / land).
- [x] An abstract entity `AbsEntity` that regroups the core, expected methods for an `Entity` : box, pose definition, and hackagame methods. An `Entity` is a `AbsEntity` 
- [x] `Tiles`: a tile is an `Entity` interconnected with other tiles. 
- [x] a tile contains entities. The elements are positioned in the tile. 
- [x] `Map` : a map is an `AbsEntity`. It contains several tiles. Its shape (not necessarily convex) is the fusion of all contained tiles.
- [x] Initialize artist rendering: abstract entities can be rendered through an Artist object.
- [x] HackaGame (DataTree) compatible


## Tiled land Advanced :


## Multi-Agent System (MAS) framework

Agent-model is derivated from Hackagames. Agent is mainly defined by a `perception`, `decide` loop, itsel included in a `wake-up` and `sleep` super-loop.
TiledLand agents perception and actions are mainly defined regarding the capability to move in a graph-model of the environment. 

- [ ] `Agent` can decide an action to perform.
- [ ] `Land` mainly a Map, but also an Agent manager, with agents linked to the Map's entities.
- [ ] _'agent'_ vs _'behavio'_ : Think state machine...
- [ ] a 'basic' agent : with several moving strategies...
- [ ] HackaAgent: encapsulating a basic agent for distributed computing.


## Simple, but strong plan geometry

Have the posibility to swith on a C-based librairie for computations...

- [ ] Map vs Map a semantic map ie. structured tiled obj (and in oposition to GridMap).
- [x] Fast position requestest : add a grid canvas to Map get a tiles from a position (getTile at, closest, inRadius ...)
- [ ] PointCloud (potentially from Scan) to Envellope, a centered and ordered PointCloud.
- [ ] Map: Apply a grid and use it on connectClose...
- [ ] Map: Generation from Voroi, gabriel, ....
- [ ] Tile: Search for text zones (header, body, footer)
- [ ] Based on an appropriation of BOX2D c-library...
- [ ] Georeferenced solution (import GIS Data)


## Geometrical Land :

- [x] Agent's bodys: Position, clock-orientation and Convex
- [x] Grid and Hexa-grid based map initilization.
- [ ] Agents: update position and Convex function (auto-centering) (Agent: `perceive(Obs)`, `decide()` and Environement/Game/Map: `forward(agent, action)` (But on Hacka?) )
- [ ] Basic Map manipulation: doSomething ... doTeleportOn(tile, agent, group).
- [ ] Be topological: Clockdir manipulation.
- [ ] Generate map from point-graph (mesh).
- [ ] No geometry artifact on Agent and Tiles...



## Web IHM

- [x] Artist + support architectur.
- [x] SVG Support and PNG Support with Cairo.
- [ ] Interactive Simulation (Move-To)
- [ ] With Sprites


## Robotique

- [x] Transform GridMap to TiledLand.Map.
- [ ] Integrate TiledLand in Tiled ROS packages.
- [ ] Be resilent to hugly maps
- [ ] Be resilent on 'all' ".png" format. 
- [ ] Cloud point on frontiere cell (position on frontiers not cell center).
- [ ] Correction on colliding convexes paving a matter.


## HackaGames - Chopes

Catch-me if you can, from RIP-Astrid.



## HackaGames - Cofee Fleet

Multi-Path planning problem (with uncertainty).



## HackaGames - Pick'n Del

Multi-Modal (Dynamic) Pick-up and Delivery with hiden random congestion.

- [x] Carrier from Agents and World from LAnd.
- [x] Mission on market place (origin destination)
- [x] Hacka compatible GameMaster
- [x] First players and first of documentation.
- [x] Uncertainty with encumbered tiles
- [ ] Dedicated documentation on ktorz-net.github.io
- [ ] Handle seral carriers
- [ ] MultiPlayer version
- [ ] Multiple mission and - carrier capacity
- [ ] encumbered value function of population/directions


## Documentaion :

- [ ] Push tiled-land on pypip
- [ ] Specific pages.
- [ ] Write doc contents...
- [ ] labelise test cases : `fast` and `long`

**-- Board V2.0 --**


## Go efficient :

- [ ] Migrate geometry module on a _C_ library (from `box2d` or new `LibEGG` Euclidean Graspable Geometry).
- [ ] Encapsulate _Convex_ in _Motif_ object (ie. one or several join convexes)
- [ ] Migrade Map geometry function into a Texture dedicated object (collection of _Motif_).


## Rendering :

- [ ] Sprites...
- [ ] Play 2.5D world.
- [ ] Projection simple : (vertical ratio)
- [ ] Free Projection : (rotation + translation)


## Map, Tiles and Agents :

- [ ] map with _epsilon_ and _seam_ distance


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


## Explorations

- [ ] decide lib-based or independant - (Explore [igraph](https://python.igraph.org) possibilities)
- [ ] Agent Based Model (or not ?): Step engine, also in a way compatible to hackagames

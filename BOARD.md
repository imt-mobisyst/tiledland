# Board:

**-- Board V1.x.x --**

## Plan Convex Geometry :

**TiledLand** aims to model spatio-temporal entities and their interaction.
It is based on convex poligon shaping implemented in the geometric functionality.

- [x] Basic point, line, and polygon objects in 2D frame.
- [x] Simple rectangular boxing.
- [x] Main Convex object to represent a convex polygon.
- [x] Convex obj. min/max radius, and collision.
- [ ] Canva, Grid based collection of Convex Object...
- [ ] Have the posibility to swith on a C-based librairie.
- [ ] Make `Convex.initRegular()` centered on (0, 0) - with test.
- [ ] Remove rotate from Unit ?
- [ ] PointCloud (potentially from Scan) to Envellope: a centered and ordered PointCloud.
- [ ] Based on an appropriation of BOX2D c-library ?
- [ ] Georeferenced solution (import GIS Data)
- [ ] Encapsulate _Convex_ in _Motif_ object (ie. one or several join convexes)


## Artist Rendering :

On top of geometric objects, _Artist_ include functionalities to draw and produce visual rendering.
Artist is designed independant to graphical librairie, the glue is implemented in Support interface.

- [ ] Convex: Search for good text zones (header, body, footer)
- [ ] Sprites...
- [ ] Play 2.5D world.
- [ ] Projection simple : (vertical ratio)
- [ ] Free Projection : (rotation + translation)


## Tiledland collection of geometries

- [x] `Unit` the root class with group, id and shape, a convex delimitation of the element.
- [x] `Mobile`, derivated from `Unit`, disotiate a fixe outline shape reference and transformation (position, orientation).
- [ ] `Canva` element is used to better organise tiles.
- [x] Initialize artist rendering: entities can be rendered with an Artist object.


## Tiledland a Graph

The core component of TiledLand refere to the `Tiles` composing a `Map` and comtainning `Units`.

- [x] `Shaped` classes, as classes hierarchie. 
- [x] `Tiles`: a tile is an `Shaped` interconnected with other tiles. 
- [x] A tile contains entities. The elements are positioned in the tile. 
- [x] `Map` : It contains several tiles.
- [ ] `Map` derivated from `Unit. Its shape is the fusion of all contained tiles.
- [x] Implement topological clock positioning.
- [ ] append `Unit` on tile with appropriate positionning (center, then top-right corner ext.) (replace `appendCenter` by `appendPosed`)
- [ ] Map: Generation from Graph (+ read SVG)
- [ ] Map: Generation from Voroi, gabriel.
- [x] Grid and Hexa-grid based tabletop initilization.
- [ ] tabletop with _epsilon_ and _seam_ distance


## Multi-Agent System (MAS) framework

Agent-model is derivated from Hackagames. Agent is mainly defined by a `perception`, `decide` loop, itsel included in a `wake-up` and `sleep` super-loop.
TiledLand agents perception and actions are mainly defined regarding the capability to move in a graph-model of the environment. 

- [x] Agent's bodys: Position, clock-orientation and Convex
- [ ] `Agent` can decide an action to perform.
- [ ] `Land` mainly a Map, but also an Agent manager, with agents linked to the Map's entities.
- [ ] `RoadLand`, derived from `Land`, mainly dedicated to `Mobile` entities.
- [ ] `HackaGame`: MAS component natively compatible to `HackaGame` lib. Encapsulating a basic agent for distributed computing.
- [ ] _'agent'_ vs _'behavior'_ : Think state machine...
- [ ] a 'basic' agent : with several moving strategies...
- [ ] Basic Map manipulation: doSomething ... doTeleportOn(tile, agent, group).


## Tiledland Project 

- [ ] Establish code conventions.
- [ ] Create agent that check Code Convention.
- [ ] All setMethode should return self.
- [ ] That all method are directly tested like (shapeDistance).
- [ ] Push tiledland on pypip.
- [ ] Specific _imt-mobisyst_ webpages.
- [x] Write doc contents.
- [ ] labelise test cases : `fast` and `long`.

## Web IHM

- [x] Artist + support architectur.
- [x] SVG Support and PNG Support with Cairo.
- [ ] Interactive Simulation (Move-To).
- [ ] With Sprites.


## Robotique

- [x] Transform GridMap to TiledLand.Map.
- [ ] Integrate TiledLand in Tiled ROS packages.
- [ ] Be resilent to hugly tabletops.
- [ ] Be resilent on 'all' ".png" format. 
- [ ] Cloud point on frontiere cell (position on frontiers not cell center).
- [ ] Correction on colliding convexes paving a matter.


## Game - SalesRun

Concurent Sellers game. 
Make it as the default/vitrine TiledLand game.


## Game - Chopes

Catch-me if you can, from RIP-Astrid.


## Game - Cofee Fleet

Multi-Path planning problem (with uncertainty).


## Game - Pick'n Del

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


**-- Board V2.x.x --**

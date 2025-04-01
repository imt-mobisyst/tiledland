# Board V0.1:

## Get Tiledland from Hackagames.tiled

- [x] Initialize with hackagames.tiled
- [x] Initialize artist rendering
- [x] New Structure: core (Scene, Tiles and Agents), geometry and artist
- [ ] Remove dependancies to hacka.py (no POD at all)
- [ ] asDico() and fromDico() morphing


## Scene, Tiles and Agents :

- [x] Agents: Position, clock-position and Shape
- [x] Scene as collection of: group's Agents, structured on Tiles
- [x] Tiles as collection of: Agents
- [x] Abstraction on Scene: Agents could be anything...


## Scene managment :

- [ ] Basic manipulation: doSomething ... doTeleportOn( tile, agent, group ).


## Documentation :

- [ ] Presentation of Core components
- [ ] Presentation of geometry submodule
- [ ] Developpers expectation: (template from Shape + class structure + tests)


## HackaGames - Pick'n Del

Pick-up and Delivery with hiden random congestion.

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

## HackaGames - Move-It

Based on MultiPath solving problem.

- [ ] Mobile from Agent and World from Scene.
- [ ] Mission: position to reach, where something need to be done.
- [ ] NPC and Collision between mobiles.
- [ ] Hacka compatible GameMaster.
- [ ] Dedicated documentation on ktorz-net.github.io
- [ ] Handle seral Mobiles.
- [ ] MultiPlayer version.

## Geometry: 

- [ ] Agents: update position and Shape function (auto-centering)
- [ ] Scene: Generation from graphs, Voroi, gabriel, ....
- [ ] Shape: Collisions


## Simple, but strong and independant plan geometry

- [ ] Shape min/max radius, and collision.
- [ ] Shape update with a radius.
- [ ] Segment automatic tag.
- [ ] get a tiles from a position (in max radius, and closest)

## Agent Based Model:

Or not ?..

- [ ] Step engine, also in a way compatible to hackagames
 

# Board V0.2:

Board in progress...

## Migrate geometry on shapely

- [ ] Remove `Float2` and prefer `Point` from `shapely.geometry`.
- [ ] Shaped the master Shaped Object 
- [ ] Set shape attribut as `shapely.geometry.Polygon` in agent.
- [ ] asDico() and fromDico() morphing (via Pop)
- [ ] scene as STRtree ?
- [ ] Shape min/max radius, and collision.
- [ ] Shape update with a radius.
- [ ] Segment automatic tag.
- [ ] get a tiles from a position (in max radius, and closest)
- [ ] Agents: update position and Shape function (auto-centering)
- [ ] Scene: Generation from graphs, Voroi, gabriel, ....
- [ ] Shape: Collisions

## Robot compliant :

- [ ] Load a gridmap
- [ ] Social nav.


## First games : 

- [ ] Basic Scene manipulation: doSomething ... doTeleportOn(tile, agent, group).
- [ ] Be topological: Clockdir manipulation.


## Web IHM - Rendering

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


---

# HackaGames - Move-It

Based on MultiPath solving problem.

- [ ] Mobile from Agent and World from Scene.
- [ ] Mission: position to reach, where something need to be done.
- [ ] NPC and Collision between mobiles.
- [ ] Hacka compatible GameMaster.
- [ ] Dedicated documentation on ktorz-net.github.io
- [ ] Handle seral Mobiles.
- [ ] MultiPlayer version.


## Explorations

- [ ] Decide lib-based or independant scene graph - (Explore [igraph](https://python.igraph.org) possibilities)
- [ ] Agent Based Model (or not ?): Step engine, also in a way compatible to hackagames

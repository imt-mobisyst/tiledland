# Changelog

Following [KeepAChangeLog](https://keepachangelog.com/) principles.

Type of changes: **Added**, **Changed**, **Deprecated**, **Removed**, **Fixed** and **Security** to marck vulnerabilities. 

## [0.2.1] - 2026-10-02

### Added

- Changelog file

## [0.2.0] - 2026-10-02

- Refactoring of Entity and derived classes.

### Added

- Mobile class (chlid of Entity)
- Mobile build over a `outline` and `position` and `orientation` 
- Mobility shape is rebuild wen required

### Removed

- AbsEntity class

### Changed

- Entity build over a unique reference to convexshape (outline)
- Entity transformation change outline
- Tile class as child of Entity

## [0.1.6] - 2026-06-11
- Major refactor of Entity/Agent/Rendering systems.
- Integration of `msgpack` for data serialization (in tests).
- Updated Python requirement to >= 3.10.

## [0.1.5] - 2026-06-11
- Cairo references made hidden/internal.
- Grid-to-Scene conversion improvements.

## [0.1.3] - 2026-06-09
- Support for `OccupencyGrid` to Scene conversion.
- Optimization of convex merging.

## [0.1.2] - 2026-04-24
- Added `draw` method to Entity class.
- Optional Cairo dependencies support.

## [0.1.1] - 2026-04-24
- General stabilization and integration.

## [0.1.0] - 2026-02-17
- Transition to `flit_core` build system.
- Core tiling and scene generation from ROS gridmaps.
- Introduction of convex shapes for navigation.

## [0.0.1] - 2024-05-17
- Initial release.
- Basic point and segment geometry.
- Basic Tile and Joint coordinate system.

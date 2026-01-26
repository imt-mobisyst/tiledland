# Plan geometry

Basic primitive of plan geometry in TiledLand.

## Experiements on Convexly...

The main idea was to test `Convexly` (based on libGEOS) but several conclusion :

- Not well documented : it is hard to do find how to do things : i.e. change Point coordinate for instance...
- Strangely managed Object, so it is not possible to apply hineritance, and so on 
- As a result, my strategy to bypass the limitation go on re-instanciate objects, but with a huge cost on the code efficiency...

The test is saved on the `test-shapely` branch and match the `v0.1.0` version. 

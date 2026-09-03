# Entity : the root TiledLand Object

An entity is mainly an object defined by a geometrical shape (itself a convexe polygon) somewhere in the environement.

The important feature to remenber about Entities is that it is composed in fact of 2 shapes. 
The first shape - the reference shape - should remain fixe. It can be the same for several entities.
Then the second shape - the projected shape - is a copie of the reference shape at a specific location en rotation in the environement. 

Successive transformations can be destructive on shape definition. The dualality reference/projection prevents those destructions.



# Frequent Asked Question

## Install

### I have some trouble with the dependency to python bind to Cairo librairy (pycairo).

This dependency is not hardly mandatory, but all example and demonstration manipulating _PNG_ image will fail.
It is possible to dissable _pycairo_ dependency in the dependancy lists of the `pyproject.toml` file, and install your local modified version of tiledland (`pip install /path/to/your/cloned/tiledland`)
By doing so, nly _SVG_ rendering will remain available.

# Paris algorithm

Paris is a hierarchical graph clustering algorithm described in the paper:

[A Sliding-Resolution Algorithm for Hierarchical Graph Clustering](https://perso.telecom-paristech.fr/bonald/papers/paris.pdf)

by Thomas Bonald, Bertrand Charpentier, Alexis Galland and Alexandre Hollocou

## Dependency

This Python module depends on the `networkx` package,
which can be installed using `pip`.

```python
sudo pip install networkx
```

## Getting started

Hierarchical clustering of a simple graph

```python
from paris import paris
```

Toy graph 

```python
G = nx.Graph()
```

Hierarchical clustering (as a dendrogram)

```python
D = paris(G)
```

## Running the tests

Tests on real data are available as a Jupyter notebook:

```python
example.ipynb
```
  
## License


Released under the GNU General Public License v3.


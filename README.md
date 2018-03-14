# Paris algorithm

Paris is a hierarchical graph clustering algorithm described in: 
https://

## Dependency

This Python module depends on the `networkx` package,
which can be installed using `pip`.

```python
sudo pip install networkx
```

## Getting started

Hierarchical clustering of a simple graph

```python
from paris.experiments.synthetic_data import sbm
from paris.algorithms.paris import paris
```

Stochastic block model with 4 blocks of 10 nodes with internal / external average degrees = 5 / 1

```python
model = sbm(4 * [10], 5, 1)
```

Random instance of the model (as a networkx graph)

```python
G = model.generate_graph()
```
Hierarchical clustering (as a dendrogram)

```python
D = paris(G)
```

Visualization

```python
from paris.experiments.plot_tools import plot_dendrogram

plot_dendrogram(D)
```

![Alt text](images/dendrogram.png)

Extraction of the top clustering


```python
nodes = list(G.nodes())
C = top_clustering(D, nodes)
print(C)
```

[[35, 33, 34, 31, 30, 32, 36, 37, 38, 39],
[12, 10, 19, 15, 17, 14, 16, 11, 13, 18],
[6, 0, 9, 8, 3, 7, 4, 5, 1, 2],
[24, 23, 21, 29, 22, 27, 25, 28, 20, 26]]


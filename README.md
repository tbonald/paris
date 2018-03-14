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
``

Visualization

```python
from paris.experiments.plot_tools import plot_dendrogram

plot_dendrogram(D, filename = "dendrogram")
```

![Alt text](images/dendrogram.png)

Extraction of the top clustering


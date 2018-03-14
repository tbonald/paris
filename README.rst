Paris
=====

Paris is a hierarchical graph clustering algorithm described in:
https://

Dependency
----------

This Python module depends on the ``networkx`` package,
which can be installed using ``pip``.

::

    sudo pip install networkx

Getting Started
------------

Hierarchical clustering of a simple graph:

.. code:: python

	import networkx as nx
	from paris.experiments.synthetic_data import sbm

    # Stochastic block model with 4 blocks of 10 nodes
    # internal / external average degree (inside / outside blocks) = 5 / 1
    model = sbm(4 * [10], 5, 1)
    
    # Generation of a random instance
    G = model.generate_graph()
    print(nx.info(G))
    
    # Hierarchical clustering (as a dendrogram)
    D = paris(G)
    
Visualization:

.. code:: python

    from paris.experiments.plot_tools import plot_dendrogram

    plot_dendrogram(D)
    
![Alt text](images/dendrogram.jpg?raw = true "A dendrogram")


Extraction of the top clustering from the dendrogram:

.. code:: python

    from hierarchy import top_clustering

    nodes = list(G.nodes())
    C = top_clustering(D, nodes)

Extraction of the top-3 clusterings from the dendrogram:

.. code:: python

    from hierarchy import top_clusterings

    C_list = top_clusterings(D, nodes, 3)


Running the tests
--------------

Tests on both synthetic and real data are available as Jupyter notebooks:

.. code:: python

    synthetic_data.ipynb
    real_data.ipynb

  
License
-------

Released under the BSD license.


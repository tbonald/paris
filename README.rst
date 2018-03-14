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

Dendrogram of a simple graph (stochastic block model):

.. code:: python

    from synthetic_data import sbm
    from paris import paris

    model = sbm(4 * [10], 5, 1)
    G = model.create_graph()
    D = paris(G)

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


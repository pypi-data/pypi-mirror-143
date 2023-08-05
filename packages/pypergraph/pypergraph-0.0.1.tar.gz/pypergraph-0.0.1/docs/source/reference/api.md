# API

```{eval-rst}
.. only:: html

   :Release: |release|
   :Date: |today|

```

```{py:currentmodule} pypergraph
```

## Hypergraph

```{eval-rst}
.. autoclass:: Hypergraph
   :exclude-members: __init__, __new__
   
   .. autoproperty:: nodes
   .. autoproperty:: edges
   .. autoproperty:: edge_labels
   .. automethod:: add_node
   .. automethod:: add_nodes
   .. automethod:: add_edge
   .. automethod:: add_edges
   .. automethod:: remove_nodes
   .. automethod:: remove_edges
   .. automethod:: remove_parallel_edges

```

## Data access

```{eval-rst}
.. autoclass:: NodeDataAccess
   :exclude-members: __init__, __new__

   .. automethod:: __iter__
   .. automethod:: __getitem__
   .. automethod:: data

.. autoclass:: EdgeDataAccess
   :exclude-members: __init__, __new__

   .. automethod:: __iter__
   .. automethod:: __getitem__
   .. automethod:: data

```

### Optimised for the absence of parallel hyperedges

```{eval-rst}
.. autoclass:: EdgeIncidenceView
   :exclude-members: __init__, __new__

   .. automethod:: __iter__
   .. automethod:: __getitem__
   .. automethod:: data
   .. automethod:: parallel_to

.. autoclass:: SingleEdgeDataView
   :exclude-members: __init__, __new__

   .. autoproperty:: inner
   .. autoproperty:: label
   .. autoproperty:: nodes
   .. automethod:: __iter__
   .. automethod:: __getitem__

.. autoclass:: ParallelEdgeView
   :exclude-members: __init__, __new__

   .. automethod:: __iter__

```
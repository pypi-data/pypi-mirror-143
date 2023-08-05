# Tutorial

```{py:currentmodule} pypergraph
```

In this tutorial, you learn

-   how to create a {py:class}`Hypergraph`;
-   how to add nodes to a {py:class}`Hypergraph` and access node data
    attributes;
-   how to add hyperedges to a {py:class}`Hypergraph` and access hyperedge data
    attributes; and
-   how to remove nodes and hyperedges from a {py:class}`Hypergraph`.

## Creating a hypergraph

Start by creating an empty hypergraph.

```{doctest}
:skipif: ppg is None
>>> import pypergraph as ppg
>>> h = ppg.Hypergraph()
```

## Adding nodes

Add a node using {py:func}`Hypergraph.add_node`. Nodes are identified by a
*node name*, which must be a hashable object.

```{doctest}
:skipif: ppg is None
>>> h.add_node("A")
>>> h.add_node(0)
>>> try:
...     h.add_node(["not hashable"])
... except TypeError:
...     print("Cannot use unhashable object as node name")
...
Cannot use unhashable object as node name
```

Multiple nodes can be added at once using {py:func}`Hypergraph.add_nodes`.

```{doctest}
:skipif: ppg is None
>>> h.add_nodes(1, 2)
>>> h.nodes
NodeDataAccess(['A', 0, 1, 2])
```

A node may carry data attributes. Data attributes can be specified when using
{py:func}`Hypergraph.add_node` but not {py:func}`Hypergraph.add_nodes`.

```{doctest}
:skipif: ppg is None
>>> h.add_node("B", attr_dict={"special": True})
```

A node has a canonical data attribute `inner`. It may be used to store any
underlying object represented by a node. It defaults to the node name and need
not be hashable.

```{doctest}
:skipif: ppg is None
>>> inner_view = h.nodes.data()
>>> inner_view["B"]
'B'
>>> h.add_node("C", attr_dict={"inner": "This is the underlying object."})
>>> inner_view["C"]
'This is the underlying object.'
```

Data attributes can be accessed after node creation with
{py:attr}`Hypergraph.nodes`.

```{doctest}
:skipif: ppg is None
>>> special_view = h.nodes.data(attrs="special")
>>> special_view["B"]
True
>>> try:
...     special_view["C"]
... except KeyError:
...     print("Attribute was not defined for this node")
...
Attribute was not defined for this node
>>> special_view_with_default = h.nodes.data(attrs="special", default=False)
>>> special_view_with_default["B"]
True
>>> special_view_with_default["C"]
False
```

Data attributes can be modified by dictionary mutation.

```{doctest}
:skipif: ppg is None
>>> attr_mod = h.nodes.data(attrs=True)  # `True` to allow mutation
>>> attr_mod["A"]
{}
>>> attr_mod["B"]
{'special': True}
>>> attr_mod["C"]
{'inner': 'This is the underlying object.'}
>>> attr_mod["B"]["inner"] = 5
>>> inner_view["B"]
5
>>> attr_mod[0]["special"] = True
>>> special_view[0]
True
```

## Adding hyperedges

Add an undirected hyperedge using {py:func}`Hypergraph.add_edge`. Incident nodes
are denoted by the shorthand {py:class}`V`.

```{doctest}
:skipif: ppg is None
>>> V = ppg.V
>>> anon_label0 = h.add_edge(V(0, 1, 2))
```

Every hyperedge has a *hyperedge label* as an identifier. A label is provisioned
by default but can be provided explicitly. Labels must be hashable.

```{doctest}
:skipif: ppg is None
>>> h.add_edge(V(0, 2), label="explicit")
'explicit'
>>> try:
...     h.add_edge(V(0, 2), label=["item1", "item2"])
... except TypeError:
...     print("Cannot use unhashable object as hyperedge label")
...
Cannot use unhashable object as hyperedge label
```

Directed hyperedge creation uses the right shift operator `>>` to indicate
direction.

```{doctest}
:skipif: ppg is None
>>> anon_label1 = h.add_edge(V(0, 2) >> V(1))  # Hyperedge from {0, 2} to {1}
```

Multiple hyperedges can be added at once using {py:func}`Hypergraph.add_edges`.

```{doctest}
:skipif: ppg is None
>>> (anon_label2, anon_label3) = h.add_edges(V(1) >> V(0), V(0) >> V(1))
```

Hyperedges may carry data attributes. Data attributes can be specified when
using {py:func}`Hypergraph.add_edge` but not {py:func}`Hypergraph.add_edges`.

```{doctest}
:skipif: ppg is None
>>> h.add_edge(V(0) >> V(0), label="loop", attr_dict={"dummy": True})
'loop'
```

In the absence of parallel hyperedges, access data attributes via
{py:attr}`Hypergraph.edges`.

```{doctest}
:skipif: ppg is None
>>> h.edges[V(0) >> V(0)]["dummy"]
True
```

A hyperedge has a canonical data attribute `inner`. It may be used to store any
underlying object represented by a hyperedge. It defaults to the hyperedge
label, which may have been provisioned automatically, and need not be hashable.

```{doctest}
:skipif: ppg is None
>>> h.edges[V(0) >> V(0)].inner
'loop'
>>> h.add_edge(
...     V(1) >> V(1),
...     label="second_loop",
...     attr_dict={"inner": "This is a loop."},
... )
'second_loop'
>>> h.edges[V(1) >> V(1)].inner
'This is a loop.'
```

Note that {py:attr}`Hypergraph.edges` is generally only suitable for hypergraphs
without parallel hyperedges. When there are parallel hyperedges,
{py:attr}`Hypergraph.edge_labels` should be used instead.

```{doctest}
:skipif: ppg is None
>>> for i in range(3):
...     h.add_edge(
...         V(2) >> V(0, 1),
...         label=f"e_{i}",
...         attr_dict={"iteration": i, "next": i + 1},
...     )
...
'e_0'
'e_1'
'e_2'
>>> iteration_view = h.edge_labels.data(attrs="iteration")
>>> iteration_view["e_0"]
0
>>> attr_mod = h.edge_labels.data(attrs=True)
>>> attr_mod["e_1"]
{'iteration': 1, 'next': 2}
```

Creation of hyperedges will implicitly create nodes as necessary.

```{doctest}
:skipif: ppg is None
>>> h2 = ppg.Hypergraph()  # Empty hypergraph
>>> _ = h2.add_edge(V(1, 3) >> V(2))
>>> h2.nodes
NodeDataAccess([1, 3, 2])
```

## Removing nodes and hyperedges

Remove nodes using {py:func}`Hypergraph.remove_nodes`. Remove hyperedges using
{py:func}`Hypergraph.remove_edges` or
{py:func}`Hypergraph.remove_parallel_edges`. Note that removal of nodes also
removes any incident hyperedges.

```{doctest}
:skipif: ppg is None
>>> h3 = ppg.Hypergraph()
>>> h3.add_nodes(*"ABCDE")
>>> _ = h3.add_edges(
...     V("A") >> V("B"),
...     V("B") >> V("C"),
...     V("C") >> V("D"),
...     V(*"ABCD"),
...     V("D") >> V("E"),
...     V("E") >> V(*"ABCD"),
... )
>>> h3.add_edge(V("A") >> V("B"), label="second_AB")
'second_AB'
>>> h3.add_edge(V("B") >> V("C"), label="second_BC")
'second_BC'
>>> h3.nodes
NodeDataAccess(['A', 'B', 'C', 'D', 'E'])
>>> h3.remove_nodes("E")  # Also removes two hyperedges
>>> h3.nodes
NodeDataAccess(['A', 'B', 'C', 'D'])
>>> h3.edges
EdgeIncidenceView([V('A') >> V('B'), V('B') >> V('C'), V('C') >> V('D'), V('A', 'B', 'C', 'D')])
>>> h3.remove_edges("second_AB")
>>> h3.remove_parallel_edges(V("B") >> V("C"))
>>> h3.edges
EdgeIncidenceView([V('A') >> V('B'), V('C') >> V('D'), V('A', 'B', 'C', 'D')])
```

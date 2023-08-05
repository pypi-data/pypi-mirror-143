# Model

## Mathematical model

In {{ project }}, a hypergraph {math}`\mathcal{H}` consists of a pair
{math}`(\mathcal{V}, \mathcal{E})`. The set {math}`\mathcal{V}` contains the
*nodes* of the hypergraph. The set {math}`\mathcal{E} = \{e_i\}_{i \in I}` has
an index set {math}`I` and contains the *hyperedges*.

Each hyperedge may be *undirected* or *directed*.

-   An undirected hyperedge is some subset of {math}`\mathcal{V}`.
    -   That is, if {math}`e_i` is an undirected hyperedge then
        {math}`e_i = (i, N_i)` where {math}`N_i \subseteq \mathcal{V}`.
    -   The symbol {math}`N_i` represents the *nodes incident with {math}`e_i`*.
    -   We write {math}`N_i = N(e_i)`.
-   A directed hyperedge consists of a *tail* and a *head*, each of which is a
    subset of {math}`\mathcal{V}`.
    -   That is, if {math}`e_i` is a directed hyperedge then
        {math}`e_i = (i, T_i, H_i)` where
        {math}`T_i, H_i \subseteq \mathcal{V}`.
    -   The symbol {math}`T_i` represents the tail of {math}`e_i`, while
        {math}`H_i` represents the head of {math}`e_i`.
    -   We write {math}`T_i = T(e_i)` and {math}`H_i = H(e_i)`.

For avoidance of doubt, the following are possible within a hypergraph in
{{ project }}:

```{list-table}
:align: left
:header-rows: 1

*   -   Situation
    -   Description
*   -   Parallel undirected hyperedges
    -   It may be that {math}`N(e_i) = N(e_j)` for distinct {math}`i, j \in I`.
*   -   Parallel directed hyperedges
    -   It may be that {math}`(T(e_i), H(e_i)) = (T(e_j), H(e_j))` for distinct
        {math}`i, j \in I`.
*   -   Undirected loops
    -   It may be that {math}`N(e_i) = \{v\}` for some {math}`i \in I` and
        {math}`v \in \mathcal{V}`.
*   -   Directed loops
    -   It may be that {math}`T(e_i) \cap H(e_i) \neq \emptyset` for some
        {math}`i \in I`.
*   -   Degenerate undirected hyperedges
    -   It may be that {math}`N(e_i) = \emptyset` for some {math}`i \in I`.
*   -   Degenerate directed hyperedges
    -   It may be that either {math}`T(e_i) = \emptyset` or
        {math}`H(e_i) = \emptyset` for some {math}`i \in I`.

```

It is not possible to have {math}`T(e_i) = H(e_i) = \emptyset` for some
{math}`i \in I`.

## Logical data model

```{py:currentmodule} pypergraph
```

In {{ project }}, {py:class}`Hypergraph` is a container of *nodes* and
*hyperedges*.

Within a {py:class}`Hypergraph` instance, the nodes have unique
identifiers known as *names*, and the hyperedges have unique identifiers known
as *labels*. Node names and hyperedge labels must be hashable.

A hyperedge may be *undirected*, whereby it refers to one subset of the nodes.
Alternatively, a hyperedge may be *directed*, whereby it refers to two subsets
of the nodes, where one is known as the *tail* and the other as the *head*.

Each node or hyperedge has a single *underlying object*, which can be any Python
object.

Each node or hyperedge has an associated mapping representing *data attributes*.
A data attribute has a unique *name* which should be a {py:class}`str` value as
well as a *value* which can be any Python object. A given data attribute need
not be uniformly specified across nodes or hyperedges.

The ``"inner"`` data attribute represents the underlying object for the node or
hyperedge. If this is not specified, the underlying object is inferred as the
node name or hyperedge label.
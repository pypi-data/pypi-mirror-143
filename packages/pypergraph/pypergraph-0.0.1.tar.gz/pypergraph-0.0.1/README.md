# pypergraph

[![CI status](https://ci.codeberg.org/api/badges/meadow/pypergraph/status.svg)](https://ci.codeberg.org/meadow/pypergraph)
[![Documentation Status](https://readthedocs.org/projects/pypergraph/badge/?version=latest)](https://pypergraph.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://img.shields.io/pypi/v/pypergraph)](https://pypi.org/project/pypergraph/)
![Python version](https://img.shields.io/pypi/pyversions/pypergraph)

*pypergraph* is a pure Python package for representing hypergraphs of both the
directed and undirected varieties.

## Installation

pypergraph requires Python 3.7 or later.

```sh
pip install pypergraph
```

## Usage

Currently, only basic in-memory mutation of hypergraphs is possible.

```python
>>> import pypergraph as ppg
>>> V = ppg.V
>>> h = ppg.Hypergraph()
>>> h.add_node("A")
>>> h.add_edge(V(0, "A") >> V(1, 2, 3))
```

## Documentation

Documentation may be found at https://pypergraph.readthedocs.io/.

## Licence

pypergraph is released under the [MIT licence][MIT].

[MIT]: LICENSE

## Roadmap

pypergraph is still in early stages of development. The steering goal is to
reach a point where pypergraph may be used to reason about functional
dependencies and support data orchestration.

These Python packages are considered to be role models:

-   [schedula](https://github.com/vinci1it2000/schedula)
-   [NetworkX](https://github.com/networkx/networkx)

## See also

There are a handful of Python packages which can be used to represent
hypergraphs.

-   [graffunc](https://github.com/Aluriak/graffunc)
-   [`hypergraphs`](https://github.com/timvieira/hypergraphs)
-   [XGI](https://github.com/ComplexGroupInteractions/xgi)
-   [halp](http://murali-group.github.io/halp/)
-   [HyTra](https://github.com/balqui/HyTra)

At a high level, these gaps exist:

-   Support for directed hypergraphs
-   A flexible data model suitable for domain applications
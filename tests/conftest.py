import pytest
import networkx


@pytest.fixture
def simple_graph():
    """A simple graph.

      ┌───────┐
      │   1   │
      └┬────┬┬┘
       │    ││
       │    └┼───┐
       v     v   │
     ┌───┐ ┌───┐ │
     │ 2 │ │ 3 │ │
     └──┬┘ └─┬─┘ │
        │    │   │
        │   ┌┼───┘
        │   ││
        v   vv
      ┌───────┐
      │   4   │
      └───────┘
    """
    g = networkx.DiGraph()
    g.add_nodes_from([1, 2, 3, 4])
    g.add_edges_from([(1, 2), (1, 3), (3, 4), (1, 4), (2, 4)])
    return g

import networkx

import conda_depgraph.algorithms as algorithms


def test_in(simple_graph):
    assert networkx.is_isomorphic(algorithms.ingraph(simple_graph, 4, distance=10), simple_graph)
    assert tuple(algorithms.ingraph(simple_graph, 1).nodes()) == (1,)
    assert tuple(algorithms.ingraph(simple_graph, 2).nodes()) == (1, 2)


def test_out(simple_graph):
    assert networkx.is_isomorphic(algorithms.outgraph(simple_graph, 1), simple_graph)
    assert tuple(algorithms.outgraph(simple_graph, 4).nodes()) == (4,)
    assert tuple(algorithms.outgraph(simple_graph, 2).nodes()) == (2, 4)


def test_inout(simple_graph):
    other = networkx.DiGraph()
    other.add_nodes_from([1, 2, 4])
    other.add_edges_from([(1, 2), (2, 4)])
    assert networkx.is_isomorphic(algorithms.inoutgraph(simple_graph, 2), other)

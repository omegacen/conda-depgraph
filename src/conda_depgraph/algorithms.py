from networkx.algorithms.dag import descendants, ancestors
from networkx.algorithms.shortest_paths.generic import shortest_path_length
from networkx.algorithms.operators.binary import compose


def outgraph(g, source, distance=None):
    outs = descendants(g, source)
    if distance is not None:
        outs = {o for o in outs if shortest_path_length(g, source=source, target=o) <= distance}
    return g.subgraph(outs | {source})


def ingraph(g, target, distance=None):
    ins = ancestors(g, target)
    if distance is not None:
        ins = {i for i in ins if shortest_path_length(g, source=i, target=target) <= distance}
    return g.subgraph(ins | {target})


def inoutgraph(g, vertex, distance=None):
    i = ingraph(g, vertex, distance=distance)
    o = outgraph(g, vertex, distance=distance)
    return compose(i, o)

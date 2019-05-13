from asciinet import graph_to_ascii, GraphConversionError
from networkx import generate_graphml

from . import exceptions


def to_ascii(g):
    try:
        a = graph_to_ascii(g)
    except GraphConversionError as e:
        raise exceptions.RenderError(e.args)
    return a.splitlines()


def to_names(g):
    return sorted(g.nodes())


def to_graphml(g):
    return generate_graphml(g)

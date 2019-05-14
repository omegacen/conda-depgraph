import textwrap

import conda_depgraph.outputs as outputs


def test_names(simple_graph):
    assert outputs.to_names(simple_graph) == [1, 2, 3, 4]


def test_graphml(simple_graph):
    assert sum(1 for _ in outputs.to_graphml(simple_graph)) == 13


def test_ascii(simple_graph):
    generated = "\n".join(outputs.to_ascii(simple_graph))
    compare = """
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
         └───────┘   """
    assert textwrap.dedent(generated) == textwrap.dedent(compare[1:])

import textwrap


def test_nonsense_command(script_runner):
    ret = script_runner.run('conda-depgraph', 'asdfasdfasdf')
    assert not ret.success
    assert ret.stdout == ''
    assert len(ret.stderr.splitlines()) == 4


def test_nonsense_package(script_runner):
    ret = script_runner.run('conda-depgraph', 'out', 'asdfasdfasdf')
    assert not ret.success
    assert ret.stdout == ''
    assert len(ret.stderr.splitlines()) in (3, 4)
    assert "Package 'asdfasdfasdf' is not in the dependency graph" in ret.stderr


def test_nonsense_env(script_runner):
    ret = script_runner.run('conda-depgraph', '--name', 'asdfasdfasdf')
    assert not ret.success
    assert ret.stdout == ''
    assert len(ret.stderr.splitlines()) in (3, 4)
    assert "Could not find Conda environment 'asdfasdfasdf'" in ret.stderr


def test_timeout(script_runner):
    ret = script_runner.run('conda-depgraph', '--from-channels')
    assert not ret.success
    assert ret.stdout == ''
    assert len(ret.stderr.splitlines()) == 1


def test_graph(script_runner):
    ret = script_runner.run('conda-depgraph', 'out', 'conda-depgraph', 'in', 'asciinet')
    compare = """
         ┌──────────────┐
         │conda-depgraph│
         └──────┬───────┘
                │        
                v        
           ┌────────┐    
           │asciinet│    
           └────────┘    
        """
    assert ret.success
    assert textwrap.dedent(ret.stdout) == textwrap.dedent(compare[1:])


def test_names(script_runner):
    ret = script_runner.run('conda-depgraph', '--output-names', 'out', '-d 1', 'conda-depgraph', 'inout', 'asciinet')
    compare = """
        asciinet
        conda-depgraph
        networkx
        python
        """
    assert ret.success
    assert textwrap.dedent(ret.stdout) == textwrap.dedent(compare[1:])


def test_graphml(script_runner):
    ret = script_runner.run('conda-depgraph', '--output-graphml', 'out', 'conda-depgraph', 'in', 'asciinet')
    assert ret.success
    assert ret.stdout.startswith('<graphml')
    assert ret.stdout.endswith('</graphml>\n')

import functools

import click

from . import algorithms
from . import conda_facade
from . import exceptions
from . import outputs


@click.group(chain=True, invoke_without_command=True)
@click.option('--from-env', 'from_where', flag_value='env', default=True,
              help='Use package data from an environment (default).')
@click.option('--from-channels', 'from_where', flag_value='repo',
              help='Use package data from cached channels.')
@click.option('-p', '--prefix', default=None,
              help='Path to environment location (i.e. prefix).')
@click.option('-n', '--name', default=None,
              help='Name of environment.')
@click.option('--output-names', 'output', flag_value='names',
              help='Don\'t plot a graph but only return package names.')
@click.option('--output-graphml', 'output', flag_value='graphml',
              help='Return a GraphML representation of the graph.')
@click.option('--output-graph', 'output', flag_value='graph', default=True,
              help='Plot a graph (default).')
def main(*_, **__):
    """Plot Conda dependency graphs on the command line."""
    pass


@main.resultcallback()
def process_subcommands(subcommands, from_where, prefix, name, output):

    if from_where == 'env':
        try:
            prefix = conda_facade.locate_prefix(name, prefix)
        except exceptions.InputError as e:
            raise click.BadParameter(*e.args)
        g = conda_facade.env_graph(prefix)
    else:
        g = conda_facade.channelcache_graph()

    for s in subcommands:
        g = s(g)

    if output == 'names':
        of = outputs.to_names
    elif output == 'graphml':
        of = outputs.to_graphml
    else:
        of = outputs.to_ascii

    try:
        o = of(g)
    except exceptions.RenderError as e:
        raise click.ClickException(*e.args)
    for l in o:
        print(l)


def subcommand(f):
    """Decorator for arbitrarily nested subcommands."""
    def new_f(*args, **kwargs):
        def p(g):
            return f(g, *args, **kwargs)
        return p
    return functools.update_wrapper(new_f, f)


def subcommand_with_package_distance_args(f):
    """Decorator for subcommands with a package argument and a distance flag."""
    @click.argument('package')
    @click.option('-d', '--distance', default=None, type=int,
                  help='Restrict to packages at most this far away.')
    @subcommand
    @functools.wraps(f)
    def wrapper(g, package, distance):
        if package not in g:
            msg = f"Package '{package}' is not in the dependency graph."
            raise click.BadParameter(msg)
        return f(g, package, distance)
    return wrapper


@main.command(name='in')
@subcommand_with_package_distance_args
def in_command(g, package, distance):
    """Restrict to packages with a dependency on PACKAGE."""
    return algorithms.ingraph(g, package, distance=distance)


@main.command()
@subcommand_with_package_distance_args
def out(g, package, distance):
    """Restrict to dependencies of PACKAGE."""
    return algorithms.outgraph(g, package, distance=distance)


@main.command()
@subcommand_with_package_distance_args
def inout(g, package, distance):
    """Restrict to dependencies of PACKAGE and those with a dependency on it."""
    return algorithms.inoutgraph(g, package, distance=distance)


if __name__ == "__main__":
    main()

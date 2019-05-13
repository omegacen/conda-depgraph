import json
import os
import pathlib
import subprocess
import sys

import conda
import conda.exports
import networkx

from . import exceptions


def locate_prefix(name, prefix):
    if name is not None:
        prefix = locate_prefix_by_name(name)
    if prefix is None:
        prefix = os.environ.get('CONDA_PREFIX', sys.prefix)
    return prefix


def locate_prefix_by_name(name):
    # Allow user to specify name, but check the environment for an
    # existing CONDA_EXE command.  This allows a different conda
    # package to be installed (and imported above) but will
    # resolve the name using their expected conda.  (The imported
    # conda here will find the environments, but might not name
    # them as the user expects.)
    # Adapted from https://github.com/rvalieris/conda-tree.
    if name in ('base', 'root'):
        prefix = _conda_execute('info', '--base')
    else:
        info = json.loads(_conda_execute('info', '-e', '--json'))
        try:
            prefix = conda.base.context.locate_prefix_by_name(
                name=name, envs_dirs=info['envs_dirs']
            )
        except conda.exceptions.EnvironmentNameNotFound:
            msg = f"Could not find Conda environment '{name}'."
            raise exceptions.InputError(msg)
    return prefix


def channelcache_graph():
    prefix = _conda_execute('info', '--base')
    cache_dir = pathlib.Path(prefix) / 'pkgs' / 'cache'

    def package_data():
        for cache_file in cache_dir.glob('*.json'):
            repodata = json.loads(cache_file.read_text())
            yield repodata['packages']

    return _package_datas_to_graph(package_data())


def env_graph(prefix):
    linked_packages = conda.exports.linked_data(prefix=prefix)
    return _package_datas_to_graph([linked_packages])


def _conda_execute(*args):
    conda_exe = os.environ.get('CONDA_EXE', 'conda')
    output = subprocess.check_output([conda_exe, *args])
    return output.decode('utf-8').strip()


def _package_datas_to_graph(datas):
    g = networkx.DiGraph()
    for data in datas:
        for p in data.values():
            n = p['name']
            g.add_node(n)
            for d in p.get('depends', []):
                o, *_ = d.split(' ')
                g.add_edge(n, o)
    return g

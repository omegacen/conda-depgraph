==============
conda-depgraph
==============

A command-line utility to plot Conda dependency graphs.


About
=====

Visualizing the dependency graph of Conda packages comes in handy for
understanding why a parcticular package is installed. ``conda-depgraph``
plots the graph on the command line, so there's no need to fire up a Jupyter
notebook.

For example, listing all the packages that (indirectly) depend on MKL in a
particular environment is as easy as

.. code-block:: console

   $ conda depgraph in mkl

::

   ┌──────────┐ ┌──────┐
   │matplotlib│ │pyfits│
   └─┬────────┘ └───┬──┘
     │              │
     │ ┌────────────┘
     │ │
     v v
   ┌─────┐ ┌──────────┐
   │numpy│ │numpy-base│
   └──┬──┘ └─┬────────┘
      │      │
      └────┐ │
           │ │
           v v
         ┌─────┐
         │ mkl │
         └─────┘


Installation
============

``conda-depgraph`` can be installed as follows:

.. code-block:: console

   $ conda install -c omegacen conda-depgraph

It can either be installed into its own conda environment, or into the base
environment.

Installing it in the base environment has the benefit that the
``conda depgraph`` command is available in all other environments. However,
you will have to make sure that ``java`` is available on ``$PATH``.

Installing it in its own environment automatically ensures it can find ``java``,
but then you will have to activate that environment before you can run
``conda depgraph``.


Usage
=====

After installation a new Conda command is available:

.. code-block:: console

   $ conda depgraph [--help]
                    [--from-channels]
                    [--from-env [--name=<ENV_NAME>] [--prefix=<ENV_PATH>]]
                    [--output-names] [--output-graph]
                    [in [--distance=<DISTANCE>] <PACKAGE>]
                    [out [--distance=<DISTANCE>] <PACKAGE>]
                    [inout [--distance=<DISTANCE>] <PACKAGE>]

``depgraph`` can  plot dependency graphs from either cached repository data,
or from an existing Conda environment. The latter is the default behaviour. If
the target environment is not specified via either ``--name`` or ``--prefix``,
the current environment is used.

The subcommands (``in``, ``out``, ``inout``) restrict the output to a subgraph
of the full dependency graph of the environment. The subcommands can be
arbitrarily nested to iteratively restrict the output graph.


Examples
========

The direct dependencies of conda:

.. code-block:: console

   $ conda depgraph --name=base out --distance=1 conda

::

                         ┌─────────────┐
                         │    conda    │
                         └─┬─┬───┬┬┬─┬─┘
                           │ │   │││ │
         ┌─────────────────┘ │   │││ └─────────────────────────┐
         │            ┌──────┘   ││└─────────────────────┐     │
         │            │          └┼──────────┐           │     │
         │            │           │          │           │     │
         v            v           v          v           v     │
   ┌──────────┐ ┌───────────┐ ┌───────┐ ┌─────────┐ ┌────────┐ │
   │setuptools│ │ruamel_yaml│ │pycosat│ │pyopenssl│ │requests│ │
   └─────┬────┘ └─────┬─────┘ └┬──────┘ └────┬────┘ └────┬───┘ │
         │            │        │             │           │     │
         │            └──────┐ │ ┌───────────┘           │     │
         └─────────────────┐ │ │ │ ┌─────────────────────┘     │
                           │ │ │ │ │ ┌─────────────────────────┘
                           │ │ │ │ │ │
                           v v v v v v
                         ┌─────────────┐
                         │   python    │
                         └─────────────┘

The immediate neighborhood of sqlite:

.. code-block:: console

   $ conda depgraph --name=base inout --distance==1 sqlite

::

      ┌──────┐
      │python│
      └───┬──┘
          │
          v
      ┌──────┐
      │sqlite│
      └┬───┬─┘
       │   │
       │   └────┐
       │        │
       v        v
   ┌───────┐ ┌────┐
   │libedit│ │zlib│
   └───────┘ └────┘

Everything in between sqlite and ncurses:

.. code-block:: console

   $ conda depgraph --name base out sqlite in ncurses

::

   ┌──────┐
   │sqlite│
   └───┬──┘
       │
       v
   ┌───────┐
   │libedit│
   └───┬───┘
       │
       v
   ┌───────┐
   │ncurses│
   └───────┘


A list of the direct dependencies of Python, plus Python itself:

.. code-block:: console

   $ conda depgraph --name base --output-names out --distance=1 python

::

   libcxx
   libffi
   ncurses
   openssl
   pip
   python
   readline
   sqlite
   tk
   xz
   zlib

A list of all packages that require Python, plus Python itself:

.. code-block:: console

   $ conda depgraph --name base --output-names in --distance=1 python

::

   asn1crypto
   beautifulsoup4
   certifi
   cffi
   chardet
   click
   conda
   conda-build
   conda-verify
   cryptography
   filelock
   future
   glob2
   idna
   jinja2
   markupsafe
   pip
   pkginfo
   psutil
   py-lief
   pycosat
   pycparser
   pycrypto
   pyopenssl
   pysocks
   python
   python-libarchive-c
   python.app
   pytz
   pyyaml
   requests
   ruamel_yaml
   setuptools
   six
   tqdm
   urllib3
   wheel

Use data from cached channels:

.. code-block:: console

   $ conda depgraph --from-channels out --distance=1 jupyter

::

                   ┌───────────────┐
                   │    jupyter    │
                   └┬┬───┬────┬┬┬┬─┘
                    ││   │    ││││
                    ││   │    │││└──────────────────┐
           ┌────────┼┘   │    │││                   │
           │        │    │    │││                   │
           v        │    │    │││                   │
     ┌──────────┐   │    │    │││                   │
     │ipywidgets│   │    │    │││                   │
     └──┬──┬──┬─┘   │    │    │││                   │
        │  │  │     │    │    │││                   │
    ┌───┘  │  │     │    │    │││                   │
    │┌─────┘  │     │    │    │└┼─────────┐         │
    ││        └─────┼─┐  │    │ │         │         │
    ││      ┌───────┘ │  │    │ │         │         │
    ││      │         │  │    │ │         │         │
    ││      v         v  v    │ │         v         │
    ││ ┌─────────┐ ┌────────┐ │ │ ┌───────────────┐ │
    ││ │qtconsole│ │notebook│ │ │ │jupyter_console│ │
    ││ └───┬──┬──┘ └──┬─┬─┬─┘ │ │ └─────┬───┬─────┘ │
    ││     │  │       │ │ │   │ └──┐    │   │       │
    ││     │  │       │ │ │   └────┼────┼┐  │       │
    ││     │  │       │ │ └──────┐ │    ││  │       │
    │└─────┼──┼┐      │ │        │ │    ││  │       │
    │     ┌┼──┼┼──────┘ │        │ │    ││  │       │
    │     ││  ││     ┌──┼────────┼─┼────┘│  │       │
    │     ││  ││     │ ┌┼────────┼─┼─────┼──┼───────┘
    │     ││  ││     │ ││        │ │     │  │
    │     ││  vv     v vv        v v     │  │
    │     ││ ┌───────────┐  ┌─────────┐  │  │
    │     ││ │ ipykernel │  │nbconvert│  │  │
    │     ││ └─────┬─────┘  └┬────────┘  │  │
    │     ││       │         │ ┌─────────┘  │
    │     ││       └───────┐ │ │  ┌─────────┘
    │     └┼─────────────┐ │ │ │  │
    │      └───────────┐ │ │ │ │  │
    └────────────────┐ │ │ │ │ │  │
                     │ │ │ │ │ │  │
                     v v v v v v  v
                   ┌───────────────┐
                   │    python     │
                   └───────────────┘


Similiar projects
=================

* https://github.com/rvalieris/conda-tree

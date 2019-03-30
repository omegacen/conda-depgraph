==============
conda-depgraph
==============

A command-line utility to plot Conda dependency graphs.


Installation
============

It is recommended to install ``conda-depgraph`` in its own environment:

.. code-block:: console

   $ conda create -n depgraph -c omegacen conda-depgraph

Installing it in the ``base`` environment will work, but then you'll have to
be sure that ``java`` is available in ``$PATH``.


Usage
=====

After installation and activation of the environment, a new Conda command is
available:

.. code-block:: console

   $ conda depgraph [--help]
                    [--from-channels]
                    [--from-env [--name=<ENV_NAME>] [--prefix=<ENV_PATH>]]
                    [--output-names] [--output-graph]
                    [in [--distance=<DISTANCE>] <PACKAGE>]
                    [out [--distance=<DISTANCE>] <PACKAGE>]
                    [inout [--distance=<DISTANCE>] <PACKAGE>]

``depgraph`` can  plot dependency graphs from either cached repository data,
or from an existing Conda environment. If the target environment is not
specified via either ``--name`` or ``--prefix``, the current environment is
used.

The subcommands (``in``, ``out``, ``inout``) restrict the output to a subgraph
of the full dependency graph of the environment. They can be arbitrarily nested.


Examples
========

The direct dependencies of conda:

.. code-block:: console

   $ conda depgraph --name=base outgraph --distance=1 conda

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

   $ conda depgraph --name=base inoutgraph -distance==1 sqlite

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

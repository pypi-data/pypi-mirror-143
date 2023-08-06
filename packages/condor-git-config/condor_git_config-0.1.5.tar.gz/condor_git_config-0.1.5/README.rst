##################
condor-config-hook
##################

Hook to dynamically configure an HTCondor node from a ``git`` repository.

Hook Overview
#############

The hook is integrated into a Condor config file to perform the following workflow:

* Fetch a *git repository* to a *local cache*
* Use patterns to *select configuration files*
* Dynamically *include configuration* in condor

To integrate the hook, use the ``include command`` syntax in any HTCondor config file:

.. code::

    include command : condor-git-config https://git.mydomain.com/condor-repos/condor-configs.git

.. note::  Any arguments in ``include command`` are passed directly to the program, without invoking a shell.
           This means that escapes and quotes required for passing arguments on the shell must **not**
           be used in the configuration.

Usage Notes
###########

The hook requires at least Python 3.6 to run. A list of options is available by passing ``-h`` or ``--help`` to the executable.

Installation
------------

Installation provides the ``condor-git-config`` executable.
All other dependencies are installed automatically.

Stable release version

.. code:: bash

    pip3 install condor_git_config

Current development version

.. code:: bash

    pip3 install git+https://github.com/MatterMiners/condor-git-config.git

We recommend to install the hook to a
`virtual environment <https://docs.python.org/3/library/venv.html>`_.
However, the hook is simple enough to not disturb global environments.

Configuration Selection
-----------------------

By default, ``condor-git-config`` will not recurse into sub-directories.
Only top-level files that end in ``.cfg`` are included automatically.

Which files to use can be controlled by arguments that provide regular expression
patterns to include/exclude files and whether to recurse into directories.

In addition, an HTCondor macro is created that points to the root path of the cache.
This allows top-level files to easily ``include:`` files from sub-directories.

Conditional Inclusion
:::::::::::::::::::::

Use ``--blacklist`` to exclude files by relative name and
``--whitelist`` to add exceptions to blacklisted names.

This allows you to have additional configuration, which is conditionally integrated.
For example, consider the following git repository tree:

.. code::

    |- commong.cfg
    |- security.cfg
    |- aaaron-cloud.cfg
    |- aaaron-cloud/
    |  |- overwrites.cfg
    |  |- proxy.cfg
    |- beebee-cloud.cfg

The ``aaaron-cloud`` folder will be ignored by default.
You can conditionally include the ``*-cloud.cfg`` files like this:

.. code:: bash

    --blacklist '.*-cloud\.cfg' --whitelist 'aaaron-cloud\.cfg'

This allows you to further include the files in ``aaaron-cloud`` by using ``include`` in ``aaaron-cloud.cfg``:

.. code::

    # aaaron-cloud.cfg
    include : $(GIT_CONFIG_CACHE_PATH)/aaaron-cloud/overwrites.cfg
    include : $(GIT_CONFIG_CACHE_PATH)/aaaron-cloud/proxy.cfg

This pattern is especially useful when the whitelist is set dynamically,
e.g. by using an argument file that contains the domain name.

Argument Files
--------------

The ``condor-git-config`` executable can use the ``@``
`prefix character <https://docs.python.org/3/library/argparse.html#fromfile-prefix-chars>`_
to read arguments from files.
This allows you to prepare options externally

.. code:: bash

    $ cat /etc/condor-git-config/branch
    --branch
    aaaron-cloud

and have them used dynamically to adjust configuration

.. code::

    include command : condor-git-config @/etc/condor-git-config/branch -- https://git.mydomain.com/condor-repos/condor-configs.git

---
RLJ
---
A convenient local judge. By _rqy.

 Screenshoot_

.. _Screenshoot: https://raw.githubusercontent.com/rqy1458814497/RLJ/master/screenshoots/1.gif

.. contents::

.. section-numbering::

Install
=======

You can install it by ``pip3``.

.. code-block:: bash

 $ pip3 install --upgrade rlj

Or by ``git``

.. code-block:: bash

 $ git clone git@github.com:rqy1458814497/RLJ.git
 $ cd RLJ
 $ sudo python3 setup.py install


Usage
=====

Config File
-----------

Make a File named ``config.json``, It should include:

``Source``(optional),  ``Input``,  ``Output``,  ``#``,  ``Time Limit``,  ``Memory Limit``, ``Compiling Parameter``.

For example:

.. code-block:: json

 {
   "Source"       : "example.cpp",
   "Input"        : "example#.in",
   "Output"       : "example#.ans",
   "#"            : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
   "Time Limit"   : 1000,
   "Memory Limit" : 128
 }

A easier way is run:

.. code-block:: bash

 $ rlj --genConfig [FILE]

to generate ``config.json`` (and use the argument 'FILE' to modify its name).

Data
----

Please place all data files under the folder ``data``.

e.g. in the case of the config file above,  There should be these files in ``data``: ``example1.in``, ``example1.ans``, ``example2.in``, and so on.


Judge
-----

.. code-block:: bash

 $ rlj [-s|--slient] [-j Source | --judge Source] [-c ConfigFile] [--O2]

To judge you only need to run ``rlj``

If you want to see short output, you can run ``rlj --silent`` or ``rlj -s``

For more detail you can run ``rlj -h``.

Compiling Parameter
-------------------

No parameter is applied when compiling by default.

You can add ``Compiling Parameter`` in ``config.json``.

``--O2`` is able to be set when running. See above.

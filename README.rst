.. image:: https://travis-ci.org/traverseda/pycraft.svg?branch=master
    :target: https://travis-ci.org/traverseda/pycraft
.. image:: https://coveralls.io/repos/github/traverseda/pycraft/badge.svg?branch=master 
    :target: https://coveralls.io/github/traverseda/pycraft?branch=master 

PyCraft
=======

A community driven fork of `foglemans "Minecraft"
repo <https://github.com/fogleman/Minecraft>`_.

|#pycraft on freenode|


Motivation
----------

The original project had great ideas and implemented really cool things,
but it was primarily designed around teaching.  This project is intended
to create a community-driven engine for complicated voxel/roguelike
games which ultimately can use and extend
`GURPS <https://en.wikipedia.org/wiki/GURPS>`__.

    The Generic Universal RolePlaying System, or GURPS, is a tabletop
    role-playing game system designed to allow for play in any game
    setting.

This project will be very permissive in accepting pull-requests.


Screenshot
----------

.. figure:: screenshot.png
   :alt:

Virtual Environment (Recommended)
---------------------------------

.. code:: bash

    # create a virtual environment
    virtualenv -p python3 ~/.venv/pycraft # (or wherever)
    # you may need to add execute permissions
    chmod -R a+x ~/.venv
    # activate
    . ~/.venv/pycraft/bin/activate # on mac
    . ~/.venv/pycraft/Scripts/activate # on windows
    # deactivate (when you're done)
    deactivate

Installing
----------

.. code:: bash

    pip install -e .

**option 1:**

.. code:: bash

    pip install -e .[dev]
    # or: python3 setup.py develop
    pycraft

**option 2:**

.. code:: bash

    python -m pycraft
    # or: python3 -m pycraft

Features
--------

* Support for python 3.5
* Simple Perlin Noise terrain generator
* Object-oriented blocks system


How to Play
-----------

Moving
~~~~~~

-  W: forward
-  S: back
-  A: strafe left
-  D: strafe right
-  Mouse: look around
-  Space: jump
-  Tab: toggle flying mode

Building
~~~~~~~~

-  Selecting the type of block to create:

   -  1: brick
   -  2: grass
   -  3: sand

-  Mouse left-click: remove block
-  Mouse right-click: create block

Quitting
~~~~~~~~

-  ESC: release mouse, then close window

.. |#pycraft on freenode| image:: https://img.shields.io/badge/chat-on%20freenode-brightgreen.svg
   :target: https://kiwiirc.com/client/irc.freenode.net/#pycraft


Contributing
------------

We support and encourage contributions.



Attributions
------------

The game textures
"`Piehole <http://piehole.alexvoelk.de/>`__"
by
`Alex Voelk <http://www.alexvoelk.de/>`__
is licensed under
`CC BY 3.0 <https://creativecommons.org/licenses/by/3.0/>`__.

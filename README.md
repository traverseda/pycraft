## Overview

A fork of [foglemans "Minecraft" repo](https://github.com/fogleman/Minecraft), intended to be more aggressive in implementing new features and sacrificing some of what makes the original good for teaching.

I plan to be very permissive in accepting pull-requests. The original had a ton
of people doing cool stuff with it, but that didn't fit the vision of it being
a learning tool.

Ultimately, I'd like to see this as a generic framework for building
complicated voxel/roguelike games. I'd like to see it implementing rules
similar to [GURPS](https://en.wikipedia.org/wiki/GURPS), but we're a long way off from that.

>The Generic Universal RolePlaying System, or GURPS, is a tabletop role-playing
game system designed to allow for play in any game setting.

#### #pycraft on freenode

![](screenshot.png "")

##Running

```
# virtual environment (recommended)
virtualenv -p python3 ~/.venv/pycraft` # (or wherever)
. ~/.venv/pycraft/bin/activate # on mac
. ~/.venv/pycraft/Scripts/activate # on windows

# pip
pip install -r requirements-dev.txt

# option 1:
python setup.py develop
pycraft

# option 2:
python -m pycraft

```

## Features

This is still a very early project and doesn't offer much over the original "minecraft in 500 lines" project.

So far, we have

 * python > 3.5 only (expect to see us taking advantage of async/await)

 * Super simple perlin noise terrain generator

 * The start of an object-oriented blocks system (check out objects/default.py)

 * Permissive policy on pull requests

## How to Play

#### Moving

- W: forward
- S: back
- A: strafe left
- D: strafe right
- Mouse: look around
- Space: jump
- Tab: toggle flying mode

#### Building

- Selecting the type of block to create:
    - 1: brick
    - 2: grass
    - 3: sand
- Mouse left-click: remove block
- Mouse right-click: create block

#### Quitting

- ESC: release mouse, then close window

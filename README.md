# PyCraft

[![#pycraft on freenode](
  https://img.shields.io/badge/chat-on%20freenode-brightgreen.svg
)](https://kiwiirc.com/client/irc.freenode.net/#pycraft)

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

## Screenshot

![](screenshot.png "")

## Virtual Environment (Recommended)

```bash
# create a virtual environment
virtualenv -p python3 ~/.venv/pycraft # (or wherever)
# you may need to add execute permissions
chmod -R a+x ~/.venv
# activate
. ~/.venv/pycraft/bin/activate # on mac
. ~/.venv/pycraft/Scripts/activate # on windows
# deactivate (when you're done)
deactivate
```

## Installing

```bash
pip install -r requirements-dev.txt
```

**option 1:**
```bash
python setup.py develop
# or: python3 setup.py develop
pycraft
```

**option 2:**
```bash
python -m pycraft
# or: python3 -m pycraft
```

## Testing

```bash
# basic
py.test
# coverage report
coverage run -m py.test; coverage report
# coverage report (html)
coverage run -m py.test; coverage html
# the report should at htmlcov/index.html
```

## Features

This is still a very early project and doesn't offer much over the original "minecraft in 500 lines" project.

So far, we have
 * python > 3.5 only (expect to see us taking advantage of async/await)
 * Super simple perlin noise terrain generator
 * The start of an object-oriented blocks system (check out pycraft/objects)
 * Permissive policy on pull requests

## How to Play

### Moving

- W: forward
- S: back
- A: strafe left
- D: strafe right
- Mouse: look around
- Space: jump
- Tab: toggle flying mode

### Building

- Selecting the type of block to create:
    - 1: brick
    - 2: grass
    - 3: sand
- Mouse left-click: remove block
- Mouse right-click: create block

### Quitting

- ESC: release mouse, then close window

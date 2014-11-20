#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from chute import app
from chute.commands import Workers

manager = Manager(app)

manager.add_command('workers', Workers())
manager.add_command('assets', ManageAssets())

if __name__ == "__main__":
    manager.run()
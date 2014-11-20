#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.script import Manager

from chute import app
from chute.commands import Workers

manager = Manager(app)

manager.add_command('workers', Workers())

if __name__ == "__main__":
    manager.run()
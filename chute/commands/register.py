# -*- coding: utf-8 -*-
from flask.ext.script import Command

from ..services import RegisterBoxService


TRUTHY = ['true', 'yes', 't', '1', 1]


class Register(Command):

    def run(self, *args, **kwargs):
        """
        """
        s = RegisterBoxService()
        return s.process()

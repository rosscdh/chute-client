# -*- coding: utf-8 -*-
from flask.ext.script import Command

from ..services import BoxApiService


TRUTHY = ['true', 'yes', 't', '1', 1]


class Register(Command):

    def run(self, *args, **kwargs):
        """
        """
        s = BoxApiService()
        return s.register()

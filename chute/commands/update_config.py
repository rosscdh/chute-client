# -*- coding: utf-8 -*-
from flask.ext.script import Command, Option

import config as settings

from ..services import BoxApiService


class UpdateConfig(Command):
    def run(self, **kwargs):
        """
        """
        s = BoxApiService()
        resp = s.update_config()
        print(resp)


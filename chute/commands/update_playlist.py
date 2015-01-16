# -*- coding: utf-8 -*-
from flask.ext.script import Command, Option

from ..services import BoxApiService


class UpdatePlaylist(Command):
    def run(self, **kwargs):
        """
        """
        s = BoxApiService()
        resp = s.update_playlist()
        print(resp)

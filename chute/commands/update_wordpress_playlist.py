# -*- coding: utf-8 -*-
from flask.ext.script import Command, Option

from ..services import BoxApiService


class UpdateWordpressPlaylist(Command):
    def run(self, **kwargs):
        """
        """
        s = BoxApiService()
        resp = s.get_rss_from_wordpress()
        s.update_playlist(content=resp)


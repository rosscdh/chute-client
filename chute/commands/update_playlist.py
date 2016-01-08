# -*- coding: utf-8 -*-
from flask.ext.script import Command, Option

import config as settings

from ..services import BoxApiService


class UpdatePlaylist(Command):
    def run(self, **kwargs):
        """
        """
        s = BoxApiService()
        if getattr(settings, 'WORDPRESS_RSS_BASE_URL', None) is not None:
            resp = s.get_rss_from_wordpress()
            resp = s.update_playlist(content=resp)
        else:
            resp = s.update_playlist()
        # print(resp)
        s.download_feed()


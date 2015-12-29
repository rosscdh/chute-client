# -*- coding: utf-8 -*-
from flask.ext.script import Command, Option

from ..services import BoxApiService
from ..tasks import download_feed

BOX_SERVICE = BoxApiService()


class DownloadPlaylistMedia(Command):
    def run(self, **kwargs):
        """
        """
        download_feed(feed=BOX_SERVICE.FEED_PATH)

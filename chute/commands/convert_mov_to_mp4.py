# -*- coding: utf-8 -*-
from flask.ext.script import Command, Option

from ..services import BoxApiService


class ConvertMovToMP4(Command):
    def run(self, **kwargs):
        """
        """
        s = BoxApiService()
        resp = s.convert_mov_to_mp4()
        print(resp)


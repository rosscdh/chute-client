# -*- coding: utf-8 -*-
from flask.ext.script import Command, Option


from ..services import PusherService


class SendEvent(Command):
    def run(self, **kwargs):
        """
        """
        s = PusherService()
        resp = s.send(channel='presence', event='reload')
        print(resp)


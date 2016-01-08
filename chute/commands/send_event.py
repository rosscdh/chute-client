# -*- coding: utf-8 -*-
from flask.ext.script import Command, Option


from ..services import PusherService


class SendEvent(Command):
    def get_options(self):
        return [
            Option('-c', '--channel', dest='channel', default='presence'),
            Option('-e', '--event', dest='event', default='reload'),
        ]

    def run(self, channel, event):
        """
        """
        s = PusherService()
        resp = s.send(channel=channel, event=event)
        print(resp)


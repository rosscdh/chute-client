# -*- coding: utf-8 -*-
from flask.ext.script import Command, Option

from ..services import PusherService

import json


class SendEvent(Command):
    def get_options(self):
        return [
            Option('-c', '--channel', dest='channel', default='presence'),
            Option('-e', '--event', dest='event', default='reload'),
            Option('-d', '--data', dest='data', default={}),
        ]

    def run(self, channel, event, data):
        """
        """
        try:
            data = json.loads(data)
        except Exception as e:
            data = {}
        print data
        s = PusherService()
        resp = s.send(channel=channel, event=event, **data)
        print(resp)


# -*- coding: utf-8 -*-
from .services import ProcessFeedMediaService

from uuid import getnode as get_mac

import json
import requests


def download_feed(feed, *args, **kwargs):
    s = ProcessFeedMediaService(feed=open(feed, 'r'))
    s.process()

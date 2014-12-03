# -*- coding: utf-8 -*-
from uuid import getnode as get_mac

import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

CORE_SERVER_ENDPOINT = 'http://localhost:8000/api/v1/'  # must have / at end
MAC_ADDR = get_mac()

PUSHER_APP_ID = 79947
PUSHER_KEY = 'cf7fc048e21bd39e6f82'
PUSHER_SECRET = '01d612aade08edc9dfde'

STATIC_PATH = os.path.join(_basedir, 'static')
MEDIA_PATH = os.path.join(_basedir, '../', 'media')
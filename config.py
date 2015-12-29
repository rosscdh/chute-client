# -*- coding: utf-8 -*-
from uuid import getnode as get_mac

import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
PROJECT_ENV = 'dev'

CORE_SERVER = 'http://magnificent.de/'  # must have / at end
CORE_SERVER_ENDPOINT = '%sapi/v1/' % CORE_SERVER  # must have / at end
MAC_ADDR = get_mac()

PUSHER_APP_ID = 79947
PUSHER_KEY = 'cf7fc048e21bd39e6f82'
PUSHER_SECRET = '01d612aade08edc9dfde'

STATIC_PATH = os.path.join(_basedir, 'static')
BOWER_COMPONENTS_ROOT = os.path.join(_basedir, 'bower_components')

MEDIA_PATH = os.path.join(_basedir, 'media')


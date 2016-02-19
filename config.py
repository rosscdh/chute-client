# -*- coding: utf-8 -*-
from uuid import getnode as get_mac

import os
import json

_basedir = os.path.abspath(os.path.dirname(__file__))

CONFIG_JSON = {}

try:
    with open('config.json', 'r') as config_file:
        CONFIG_JSON = json.load(config_file)
except:
    pass

DEBUG = True
PROJECT_ENV = 'dev'

CORE_SERVER = 'http://magnificent.de'  # must have / at end
CORE_SERVER_ENDPOINT = '%s/api/v1/' % CORE_SERVER  # must have / at end
MAC_ADDR = get_mac()

#WORDPRESS_RSS_BASE_URL = 'http://taskrocket.info' # MUST NOT have a /
WORDPRESS_RSS_BASE_URL = CONFIG_JSON.get('wordpress_url')
WORDPRESS_RSS_CATEGORY = None
WORDPRESS_RSS_NUM_ITEMS = 100

PUSHER_APP_ID = '79947'
PUSHER_KEY = 'cf7fc048e21bd39e6f82'
PUSHER_SECRET = '01d612aade08edc9dfde'

DIST_PATH = os.path.join(_basedir, 'dist')
STATIC_PATH = os.path.join(_basedir, 'static')
BOWER_COMPONENTS_ROOT = os.path.join(_basedir, 'bower_components')

MEDIA_PATH = os.path.join(_basedir, 'media')


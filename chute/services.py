# -*- coding: utf-8 -*-
"""
Services to

1. Download a video and register it with the index.html once completed
"""
import config as settings

import os
import requests


class DownloadVideoService(object):
    def __init__(self, video, **kwargs):
        self.video = video

    def process(self, **kwargs):
        video_url = kwargs.pop('video_url', self.video.get('url'))

        filename = os.path.basename(video_url)
        file_path = os.path.join(settings.STATIC_PATH, filename)
        
        with open(file_path, 'wb') as handle:
            resp = requests.get(video_url, stream=True)

            if not resp.ok:
                raise Exception('Download Error: %s' % video_url)

            for block in resp.iter_content(1024):
                if not block:
                    break

                handle.write(block)

        return file_path, True

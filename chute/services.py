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

        message = 'File already exists: %s' % filename

        if not os.path.exists(file_path):
            try:
                self.save(video_url, file_path)
                message = 'File downloaded: %s' % filename

            except Exception as e:
                message = 'File not downloaded: %s' % e
            

        return file_path, message

    def save(self, video_url, file_path):
        with open(file_path, 'wb') as handle:
            resp = requests.get(video_url, stream=True)

            if not resp.ok:
                raise Exception('Download Error: %s %s' % (resp, video_url))

            for block in resp.iter_content(1024):
                if not block:
                    break

                handle.write(block)

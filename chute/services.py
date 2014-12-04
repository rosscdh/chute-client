# -*- coding: utf-8 -*-
"""
Services to

1. Download a video and register it with the index.html once completed
"""
import config as settings

import os
import json
import requests


class BoxApiService(object):
    """
    Service registers this box/client with the core server
    """
    FEED_PATH = os.path.join(settings.MEDIA_PATH, 'playlist.json')
    MAC_ADDRESS = settings.MAC_ADDR

    def register(self, **kwargs):
        project_slug = kwargs.get('project', None)  # project_slug to register with
        playlist_uuid = kwargs.get('playlist', True)  # playlist uuid to register with

        data = {
            'mac_address': self.MAC_ADDRESS,
            'project': project_slug,
        }
        url = '%s%s' % (settings.CORE_SERVER_ENDPOINT,
                        'box/register/')
        return requests.post(url, data=data)

    def playlist(self, **kwargs):
        store = kwargs.get('store', True)  # save the playlist locally

        url = '%s%s' % (settings.CORE_SERVER_ENDPOINT,
                        'box/%s/playlist/' % settings.MAC_ADDR)

        resp = requests.get(url)
        data = resp.json()

        if store is True:
            with open(self.FEED_PATH, 'w') as playlist:
                playlist.write(resp.content)

        return data


class ProcessFeedMediaService(object):
    def __init__(self, feed):
        if not getattr(feed, 'read', False):
            raise Exception('Expecting an open file ready for reading')

        self.feed = json.loads(feed.read().decode('utf8'))

    def process(self):
        for i, item in enumerate(self.feed):

            for url in [item.get('picture'), item.get('video')]:
                if url:
                    media = {
                        'id': item.get('id'),
                        'url': url
                    }

                    s = DownloadMediaService(video=media)
                    file_path, download_result = s.process()

                    print('File: %s Download Result: %s' % (file_path, download_result))


class DownloadMediaService(object):
    def __init__(self, video, **kwargs):
        self.video = video

    def process(self, **kwargs):
        video_url = kwargs.pop('video_url', self.video.get('url'))

        filename = os.path.basename(video_url)
        file_path = os.path.join(settings.MEDIA_PATH, filename)

        message = 'File already exists: %s' % filename

        if not os.path.exists(file_path):
            try:
                self.save(video_url, file_path)
                message = 'File downloaded: %s' % filename

            except Exception as e:
                message = 'File not downloaded: %s' % e

        #logger.info('%s : %s ' % (file_path, message))
        return file_path, message

    def save(self, video_url, file_path):
        #logger.debug('Saving %s to %s' % (video_url, file_path))
        with open(file_path, 'wb') as handle:
            resp = requests.get(video_url, stream=True)

            if not resp.ok:
                raise Exception('Download Error: %s %s' % (resp, video_url))

            for block in resp.iter_content(1024):
                if not block:
                    break

                handle.write(block)

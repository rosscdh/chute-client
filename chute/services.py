# -*- coding: utf-8 -*-
"""
Services to

1. Download a video and register it with the index.html once completed
"""
import config as settings

from tomorrow import threads
from collections import Counter

from .mixins import RssReaderMixin

from flask import render_template
from pusher import Pusher

import sh

import os
import re
import json
import urllib2
import requests
import subprocess


class BoxApiService(RssReaderMixin, object):
    """
    Service registers this box/client with the core server
    """
    FEED_PATH = os.path.join(settings.MEDIA_PATH, 'playlist.json')
    MAC_ADDRESS = settings.MAC_ADDR

    def calculate_wait_for(self, corpus):
        """
        Method to calculate the amount of time to display this item, based on
        150 wpm (floor avg reading speed) * 1.5
        """
        words = re.findall(r'\w+', corpus.lower())
        count = Counter(words)
        total = count.values()
        base = (150 / sum(total))
        return (150 / base) if base > 0 else 30

    def register(self, **kwargs):
        project_slug = kwargs.get('project', None)  # project_slug to register with

        data = {
            'mac_address': self.MAC_ADDRESS,
            'project': project_slug,
        }
        url = '%s%s' % (settings.CORE_SERVER_ENDPOINT,
                        'box/register/')

        resp = requests.post(url, data=data)

        return resp

    def update_config(self, **kwargs):
        s = UpdateConfigService()
        s.process()

    def render(self, **kwargs):
        self.update_playlist(content=self.get_rss_from_wordpress())

        playlist = self.read_playlist()

        context = {'project_json': json.dumps(playlist.get('project', {})),
                   'feed_json': json.dumps(playlist.get('feed', [])),
                   'mac_addr': settings.MAC_ADDR,
                   'settings': json.dumps({
                       'CORE_SERVER': settings.CORE_SERVER,
                       'CORE_SERVER_ENDPOINT': settings.CORE_SERVER_ENDPOINT,
                       'MAC_ADDRESS': settings.MAC_ADDR,
                   }),
                   'pusher': {
                       'PUSHER_KEY': settings.PUSHER_KEY,
                    }}

        rendered_template = render_template('player.html', **context).encode('utf-8')

        if os.path.isdir(settings.DIST_PATH) is False:
            os.makedirs(settings.DIST_PATH)

        target_file = os.path.join(settings.DIST_PATH, 'index.html')

        print('Writing to: %s' % target_file)

        with open(target_file, 'w') as output_file:
            output_file.write(rendered_template)

        return rendered_template

    def update_playlist(self, **kwargs):
        content = kwargs.get('content', None)

        if content is not None:
            data = json.loads(content)

        else:
            # we have no content passed in then get it form teh playlist server
            url = '%s%s' % (settings.CORE_SERVER_ENDPOINT,
                            'box/%s/playlist/' % settings.MAC_ADDR)
            print url
            resp = requests.get(url)
            data = resp.json()
            content = resp.content

        if data:
            with open(self.FEED_PATH, 'w') as playlist:
                playlist.write(content)
            try:
                pusher_service = PusherService()
                pusher_service.send(channel='presence', event='reload')
            except:
                pass

        return data

    def download_feed(self, **kwargs):
        s = ProcessFeedMediaService(feed=open(kwargs.get('feed', self.FEED_PATH), 'r'))
        return s.process()

    def read_playlist(self, **kwargs):
        return json.loads(open(self.FEED_PATH, 'r').read().decode('utf-8'))

    def convert_mov_to_mp4(self, **kwargs):
        options = {
            'media_path': settings.MEDIA_PATH,
            'from_format': kwargs.get('from_format', 'mov'),
            'to_format': kwargs.get('to_format', 'mp4'),
            'codec': kwargs.get('codec', 'libx264'),
            'threads': kwargs.get('threads', 2),
            'cpu': kwargs.get('cpu', 2),
        }
        cmd = "find {media_path} -name '*.{from_format}' -exec bash -c 'avconv -i \"$0\" -c:v {codec} -strict experimental -cpu-used {cpu} -threads {threads} \"${{0%%.{from_format}}}.{to_format}\"' {{}} \\;".format(**options)
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()


class ProcessFeedMediaService(object):
    def __init__(self, feed):
        if not getattr(feed, 'read', False):
            raise Exception('Expecting an open file ready for reading')

        self.feed = json.loads(feed.read().decode('utf8'))

    def process(self):
        """
        download media extracted from the feed
        """
        for i, item in enumerate(self.feed.get('feed', [])):

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

        filename = os.path.basename(urllib2.urlparse.urlparse(video_url).path)
        file_path = os.path.join(settings.MEDIA_PATH, filename)

        message = 'File already exists: %s' % filename

        try:
            self.save(video_url, file_path)
            message = 'File downloaded: %s' % filename

        except Exception as e:
            message = 'File not downloaded: %s' % e

        return file_path, message

    def save(self, video_url, file_path):
        resp = requests.get(video_url, stream=True)

        if not resp.ok:
            raise Exception('Download Error: %s %s' % (resp, video_url))

        with open(file_path, 'wb') as handle:
            for block in resp.iter_content(1024):
                if not block:
                    break

                handle.write(block)


class PusherService(object):
    def __init__(self, **kwargs):
        self.client = Pusher(app_id=getattr(settings, 'PUSHER_APP_ID'),
                             key=getattr(settings, 'PUSHER_KEY'),
                             secret=getattr(settings, 'PUSHER_SECRET'),
                             host=u'127.0.0.1', port=4567, ssl=False)

    def send(self, channel, event, **kwargs):
        return self.client.trigger(unicode(channel), unicode(event), kwargs)


class UpdateConfigService(object):
    """
    Service to download and run config commands locally
    """
    url = '%s%s' % (settings.CORE_SERVER_ENDPOINT,
                    'box/%s/config/' % settings.MAC_ADDR)

    def process(self):
        #resp = requests.get(self.url)
        self.run_ansible()

    #@threads(1)
    def run_ansible(self):
        output = sh.ansible('all -i all -c local -m shell -a "echo hello world"')
        print(output)



# -*- coding: utf-8 -*-
from .services import DownloadMediaService
from .services import ProcessFeedMediaService

from uuid import getnode as get_mac

import json
import requests


def download_feed(feed, *args, **kwargs):
    s = ProcessFeedMediaService(feed=open(feed, 'r'))
    s.process()


def download_video(data, *args, **kwargs):
    callback_webhook = data.get('callback_webhook')

    results = []
    import pdb;pdb.set_trace()
    for i, item in enumerate(data.get('media', [])):

        video_id = data.get('video_id', None)

        video = {
            'id': video_id,
            'url': item,
        }

        service = DownloadMediaService(video=video)
        file_path, download_result = service.process()

        results.append({"file_path": file_path, "result": download_result})

        if callback_webhook:
            # Post out to callback
            requests.post(callback_webhook, json.dumps({
                'job_id': None,
                'mac': get_mac(),
                'video_id': video_id,
                'result': download_result,
            }), headers={'content-type': 'application/json'})

    return results

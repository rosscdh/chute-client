# -*- coding: utf-8 -*-
from .services import DownloadVideoService

import json
import requests


def download_video(data, *args, **kwargs):
    callback_webhook = data.get('callback_webhook')

    results = []

    for i, item in enumerate(data.get('media', [])):

        video_id = data.get('video_id', None)

        video = {
          'id': video_id,
          'url': item,
        }

        service = DownloadVideoService(video=video)
        file_path, download_result = service.process()

        results.append({"file_path": file_path, "result": download_result})

        if callback_webhook:
            # Post out to callback
            requests.post(callback_webhook, json.dumps({
              'job_id': None,
              'video_id': video_id,
              'result': download_result,
            }), headers={'content-type': 'application/json'})

    return results

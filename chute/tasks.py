# -*- coding: utf-8 -*-
from .services import DownloadVideoService

import requests


def download_video(data, *args, **kwargs):
    callback_webhook = data.get('callback_webhook')

    results = []

    for i, item in enumerate(data.get('media', [])):

        video_id = data.get('id', None)

        video = {
          'id': video_id,
          'url': item,
        }

        service = DownloadVideoService(video=video)
        file_path, result = service.process()

        results.append({"file_path": file_path, "result": result})

        if callback_webhook:
            # Post out to callback
            requests.post(callback_webhook, data={
              'queue_id': None,
              'video_id': video_id,
              'file_path': file_path, 
              'result': result,
            })

    return results

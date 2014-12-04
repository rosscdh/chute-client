# -*- coding: utf-8 -*-
"""
Views to provide api endpoints that:

1. PATCH /api/config/update/ {"url": "/url/to/find/new/config.py"} - passed to a service that connects and downloads the new values
2. POST|PATCH|DELETE /api/media/(:uuid/)? {Media dict} - passes new media elements to be appended to the playlist after downloading required videos
"""
from flask import Blueprint, request, render_template

from flask.ext import restful
from flask.ext.rq import get_queue
from flask.ext.classy import FlaskView

from .services import BoxApiService
from .tasks import download_feed, download_video

import config as settings

import json


class IndexView(FlaskView):
    def get(self):
        s = BoxApiService()
        playlist = s.playlist(store=True)

        get_queue().enqueue(download_feed, feed=s.FEED_PATH)

        return render_template('player.html',
                project_json=json.dumps(playlist.get('project', {})),
                feed_json=json.dumps(playlist.get('feed', [])),
                mac_addr=settings.MAC_ADDR,
                settings=json.dumps({
                    'CORE_SERVER': settings.CORE_SERVER,
                    'CORE_SERVER_ENDPOINT': settings.CORE_SERVER_ENDPOINT,
                    'MAC_ADDRESS': settings.MAC_ADDR,
                }),
                pusher={
                    'PUSHER_KEY': settings.PUSHER_KEY,
                })


base_blueprint = Blueprint('base', __name__, template_folder='templates')


class DownloadMediaEndpoint(restful.Resource):
    def post(self):
        data = request.json

        job = get_queue().enqueue(download_video, job_id='1234-123', data=data)

        return {
            'job': {
                'id': job.id,
                'status': job.get_status(),
                'is_started': job.is_started,
            }
        }, 202


blueprint = Blueprint('api', __name__)
api = restful.Api(blueprint, prefix='/api')
api.add_resource(DownloadMediaEndpoint, '/download')

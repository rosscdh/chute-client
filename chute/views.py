# -*- coding: utf-8 -*-
"""
Views to provide api endpoints that:

1. PATCH /api/config/update/ {"url": "/url/to/find/new/config.py"} - passed to a service that connects and downloads the new values
2. POST|PATCH|DELETE /api/media/(:uuid/)? {Media dict} - passes new media elements to be appended to the playlist after downloading required videos
"""
from flask import Blueprint, request, render_template, url_for, Response

from flask.ext import restful
from flask.ext.rq import get_queue
from flask.ext.classy import FlaskView


from .tasks import download_feed, download_video


import config as settings

# import flask_wtf
# from wtforms import validators
import os
import json

# class MediaDownloadValidator(flask_wtf.Form):
#     callback_webhook = wtforms.validators.URL('callback_webhook', require_tld=False, validators=[validators.DataRequired()])
#     video_id = wtforms.validators.UUID('video_id', validators=[validators.DataRequired()])
#     media = wtforms.validators.UUID('video_id', validators=[validators.DataRequired()])


class IndexView(FlaskView):
    def get(self):
        project_path = os.path.join(settings.MEDIA_PATH, 'project.json')
        feed_path = os.path.join(settings.MEDIA_PATH, 'feed.json')

        job = get_queue().enqueue(download_feed, feed=feed_path)

        return render_template('player.html',
                project_json=open(project_path).read().decode('utf8'),
                feed_json=open(feed_path).read().decode('utf8'))


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


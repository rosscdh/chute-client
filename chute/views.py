# -*- coding: utf-8 -*-
"""
Views to provide api endpoints that:

1. PATCH /api/config/update/ {"url": "/url/to/find/new/config.py"} - passed to a service that connects and downloads the new values
2. POST|PATCH|DELETE /api/media/(:uuid/)? {Media dict} - passes new media elements to be appended to the playlist after downloading required videos
"""
from flask import Blueprint, request, redirect, url_for, render_template, flash

from flask.ext import restful
from flask.ext.rq import get_queue
from flask.ext.classy import FlaskView

from .services import BoxApiService
from .tasks import download_feed
from .forms import ConfigForm

from collections import namedtuple

import config as settings

import sh
import json

BOX_SERVICE = BoxApiService()


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class IndexView(FlaskView):
    def get(self):
        playlist = BOX_SERVICE.read_playlist()

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


class ConfigView(FlaskView):
    def get(self):
        CONFIG_JSON = {}

        try:
            with open('config.json', 'r') as config_file:
                CONFIG_JSON = json.load(config_file)
        except:
            pass

        form = ConfigForm(obj=Struct(**CONFIG_JSON),
                          csrf_enabled=False)
        return render_template('config.html', form=form)

    def post(self, *args, **kwargs):
        form = ConfigForm(request.form, csrf_enabled=False)
        if form.validate():

            with open('config.json', 'w') as config_file:
                config_file.write(json.dumps(form.data))

            flash('Sucess, updated config')

            # Restart the service
            # this will kill the process
            sh.sudo('supervisorctl restart chute-client')

            return redirect('/config/')
        return render_template('config.html', form=form)

    def after_post(self, response):
        """
        Restart the service
        """
        return response


base_blueprint = Blueprint('base', __name__, template_folder='templates')


class UpdatePlaylistEndpoint(restful.Resource):
    def post(self):
        BOX_SERVICE.update_playlist()

        return {
        }, 202


class DownloadMediaEndpoint(restful.Resource):
    def post(self):
        data = request.json

        job = get_queue().enqueue(download_feed, feed=BOX_SERVICE.FEED_PATH)

        return {
            'job': {
                'id': job.id,
                'status': job.get_status(),
                'is_started': job.is_started,
            }
        }, 202


blueprint = Blueprint('api', __name__)
api = restful.Api(blueprint, prefix='/api')
api.add_resource(UpdatePlaylistEndpoint, '/download/playlist')
api.add_resource(DownloadMediaEndpoint, '/download/playlist/media')

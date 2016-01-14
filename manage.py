#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from chute import app
from chute.commands import Workers, Register, UpdatePlaylist, UpdateWordpressPlaylist, DownloadPlaylistMedia, ConvertMovToMP4, SendEvent, UpdateConfig

manager = Manager(app)

manager.add_command('workers', Workers())
manager.add_command('assets', ManageAssets())
manager.add_command('register', Register())
manager.add_command('update_playlist', UpdatePlaylist())
manager.add_command('update_config', UpdateConfig())
manager.add_command('update_playlist_from_wordpress', UpdateWordpressPlaylist())
manager.add_command('download_playlist_media', DownloadPlaylistMedia())
manager.add_command('convert_mov_to_mp4', ConvertMovToMP4())
manager.add_command('send_event', SendEvent())


if __name__ == "__main__":
    manager.run()

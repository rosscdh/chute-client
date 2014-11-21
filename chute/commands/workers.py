# -*- coding: utf-8 -*-
from flask.ext.rq import get_worker
from flask.ext.script import Command, Manager, Option

TRUTHY = ['true', 'yes', 't', '1', 1]


class Workers(Command):

    option_list = (
        Option('--queues', '-q', dest='queues', default='default low high'),
        Option('--seperate-threads', '-t', dest='seperate_threads', default=False),
    )

    def run(self, seperate_threads, queues, *args, **kwargs):
        """
        Accepts a list of queues to run python manage.py workers default high low
        Otherwise will just start on default
        --seperate-threads (-t) for a seperate thread per worker
        """
        if seperate_threads in TRUTHY:
            for worker in args:
                get_worker(worker).work(True)
        else:
            get_worker(*queues.split(' ')).work(True)

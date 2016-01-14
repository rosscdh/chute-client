# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField
from wtforms import validators


class ConfigForm(Form):
    wordpress_url = StringField(label='Wordpress Feed URL',
                                validators=[validators.URL(),
                                            validators.Required()])

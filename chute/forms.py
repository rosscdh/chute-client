# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms import validators


class ConfigForm(Form):
    wordpress_url = StringField(label='Wordpress Feed URL',
                                validators=[validators.URL(),
                                            validators.Required()])
    location = StringField(label='Location - lat,long or address',
                           validators=[validators.Required()])
    unit = SelectField(label='Temperature Unit',
                       choices=[('c', 'Centigrade'), ('f', 'Fahrenheit')])

# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import sys
from datetime import date

import yaml


from django.db import models
from django.db.models.loading import cache
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _

from django.conf import settings


app_module = __name__.replace('.models', '')


class ModelFuncMixin(object):
    def __str__(self):
        return u"{0}".format(self._meta.fields[1].value_to_string(self))

    @classmethod
    def field_name(cls, field):
        return cls._meta.get_field(field).verbose_name

    def get_absolute_url(self):
        url_name = ''.join([app_module, ':',
            self.__class__.__name__.lower(), ':', 'detail'])
        return reverse(url_name, kwargs={'pk': self.pk})


class CustomModelTypes(object):

    @staticmethod
    def int(value):
        return models.IntegerField(verbose_name=_(value),)

    @staticmethod
    def char(value):
        return models.CharField(max_length=100,
            verbose_name = _(value),)

    @staticmethod
    def date(value):
        return models.DateField(auto_now=False, auto_now_add=False,
            verbose_name = _(value),)

    yaml_types = {
        'char': 'CharField',
        'int': 'IntegerField',
        'date': 'DateField',
    }


u_p23 = lambda s: s.decode('utf-8') if settings.PYTHON_VERSION_INFO == 3 else s


class ModelGenerator():
    def __init__(self, file, serializer):
        self.file = file
        self.serializer = serializer

    def __iter__(self):
        self.app = __name__
        self.schema = self.get_model_specification()
        return self

    def __next__(self):
        return self.next()

    def next(self):
        while self.schema:
            schema = self.schema.popitem()
            return self.set_model_cls(schema)
        raise StopIteration

    def get_model_specification(self):
        if self.serializer == 'yaml':
            try:
                schema = yaml.load(open(
                    os.path.join(settings.BASE_DIR,self.file)))
            except Exception as e:
                print(e)
        else:
            raise Exception('unknown serializer')
        return schema

    def set_model_cls(self, schema):
        table_name = schema[0].capitalize()

        class Meta:
            verbose_name = _(schema[1]['title'])
            verbose_name_plural = _(schema[1]['title'])

        attrs = {
            u_p23(b'Meta'): Meta,
            u_p23(b'__module__'): __name__,
        }
        for field in schema[1]['fields']:
            attrs.update({field['id']:
                getattr(CustomModelTypes, field['type'])(field['title'])})

        try:
            del cache.app_models[self.app][table_name]
        except KeyError:
            pass

        Model = type(table_name, (ModelFuncMixin, models.Model,), attrs)

        setattr(sys.modules[__name__], table_name, Model)
        #globals()[table] = Model

        return Model



tables = []
for model in ModelGenerator(os.path.join(
            settings.BASE_DIR, 'model.yaml') , 'yaml'):
    tables.append(model)

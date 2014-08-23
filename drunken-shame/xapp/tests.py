#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import yaml

from django.utils.six.moves import zip
from django.core.urlresolvers import resolve
from django.test import TestCase

from django.conf import settings

# Create your tests here.




class SmokeTest(TestCase):

    def test_home_url(self):
        #found = resolve('/')
        pass

    def test_admin_url(self):
        #found = resolve('/admin/')
        pass

class ModelTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_yaml_mapping(self):
        yaml_f = yaml.load(open(os.path.join(settings.BASE_DIR,'model.yaml')))

        from xapp.models import tables

        for model_table, yaml_table in zip(tables,
                      [yaml_table for yaml_table in yaml_f]):
            self.assertEqual(yaml_table.capitalize(), model_table.__name__)
            self.assertEqual(yaml_f[yaml_table]['title'],
                model_table._meta.verbose_name)

            for model_field, yaml_field in zip(
                  [model_field for model_field in model_table._meta.fields
                      if model_field.name!='id'],
                  [yaml_field for yaml_field in yaml_f[yaml_table]['fields']]
            ):
                self.assertEqual(model_field.name, yaml_field['id'])
                self.assertEqual(model_field.verbose_name, yaml_field['title'])

                from xapp.models import CustomModelTypes
                self.assertEqual(model_field.__class__.__name__,
                    CustomModelTypes.yaml_types[yaml_field['type']])
#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import json

from django.utils.six.moves import zip
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.utils import unittest
from django.test.client import Client

from django.conf import settings


class ModelTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_yaml_mapping(self):
        from xapp.models import tables
        from xapp.models import ModelGenerator
        yaml_f = ModelGenerator.yaml_ordered_load(
            open(os.path.join(settings.BASE_DIR, 'model.yaml')),)

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

    def test_users(self):
        from xapp.models import tables
        from xapp.models import Users
        d = {'name':'A', 'paycheck':'10', 'date_joined': '2014-01-01'}
        Users.create_from_dict(d)
        d = {'name':'B', 'paycheck':'20', 'date_joined': '01/01/2014'}
        Users.create_from_dict(d)
        d = {'name':'C', 'paycheck':'30', 'date_joined': '02-01-2014'}
        Users.create_from_dict(d)

        self.assertEqual(Users.objects.filter(name='A').count(), 1)

        self.assertEqual(Users.objects.all()[0]._meta.verbose_name,
            u'Пользователи')
        self.assertEqual(str(Users.objects.all()[0]),
            u'A')
        self.assertEqual(str(Users.objects.all()[1]),
            u'B')
        self.assertEqual(str(Users.objects.all()[2]),
            u'C')
        self.assertEqual(Users.objects.all()[0].field_name('name'),
            u'Имя')
        self.assertEqual(Users.objects.all()[0].field_name('paycheck'),
            u'Зарплата')
        self.assertEqual(Users.objects.all()[0].field_name('date_joined'),
            u'Дата поступления на работу')
        N = None
        for index in range(len(Users.objects.all()[0].get_all_tables())):
            if Users.objects.all()[0].get_all_tables()[index]['sheet'] == \
                    Users.objects.all()[0]._meta.verbose_name:
                N = index
        self.assertEqual(Users.objects.all()[0].get_all_tables()[N]['sheet'],
            u'Пользователи')
        self.assertEqual(Users.objects.all()[0].get_all_tables()[N]['url'],
            u'/api/users/')
        self.assertEqual(Users.objects.all()[0].get_all_tables()[N],
            {'fields': [{'id': 'id', 'name': 'ID', 'type': 'Auto'},
                {'id': 'name', 'name': 'Имя', 'type': 'Char'},
                {'id': 'paycheck', 'name': 'Зарплата', 'type': 'Integer'},
                {'id': 'date_joined', 'name': 'Дата поступления на работу',
                                                          'type': 'Date'}],
            'sheet': 'Пользователи', 'url': '/api/users/'})

    def test_rooms(self):
        from xapp.models import tables
        from xapp.models import Rooms
        d = {'department':'A', 'spots':'10'}
        Rooms.create_from_dict(d)
        d = {'department':'B', 'spots':'20'}
        Rooms.create_from_dict(d)
        d = {'department':'C', 'spots':'30'}
        Rooms.create_from_dict(d)

        self.assertEqual(Rooms.objects.filter(department='A').count(), 1)
        self.assertEqual(Rooms.objects.all()[0]._meta.verbose_name,
            u'Комнаты')
        self.assertEqual(str(Rooms.objects.all()[0]),
            u'A')
        self.assertEqual(str(Rooms.objects.all()[1]),
            u'B')
        self.assertEqual(str(Rooms.objects.all()[2]),
            u'C')
        self.assertEqual(Rooms.objects.all()[0].field_name('department'),
            u'Отдел')
        self.assertEqual(Rooms.objects.all()[0].field_name('spots'),
            u'Вместимость')
        N = None
        for index in range(len(Rooms.objects.all()[0].get_all_tables())):
            if Rooms.objects.all()[0].get_all_tables()[index]['sheet'] == \
                    Rooms.objects.all()[0]._meta.verbose_name:
                N = index
        self.assertEqual(Rooms.objects.all()[0].get_all_tables()[N]['sheet'],
            u'Комнаты')
        self.assertEqual(Rooms.objects.all()[0].get_all_tables()[N]['url'],
            u'/api/rooms/')
        self.assertEqual(Rooms.objects.all()[0].get_all_tables()[N],
            {'fields': [{'id': 'id', 'name': 'ID', 'type': 'Auto'},
              {'id': 'department', 'name': 'Отдел', 'type': 'Char'},
              {'id': 'spots', 'name': 'Вместимость', 'type': 'Integer'}],
            'sheet': 'Комнаты', 'url': '/api/rooms/'})


class RequestTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.csrf_client = Client(enforce_csrf_checks=True)

    def tearDown(self):
        pass

    def test_get_home_request(self):
        response = self.c.get('/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(u'text/html; charset=utf-8',
            response._headers['content-type'][1])
        self.assertIn('Web приложение на django', response.content.decode('utf-8'))

    def test_get_home_ajax_request(self):
        response = self.csrf_client.get('/api/963c98e6c3fb42e991e7516ddc8f1096/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertEqual(u'application/json',
            response._headers['content-type'][1])
        self.assertIn('/api/users/', response.content.decode('utf-8'))
        self.assertIn('/api/rooms/', response.content.decode('utf-8'))

    def test_get_list_rooms(self):
        from xapp.models import tables
        from xapp.models import Rooms
        d = {'department':'A', 'spots':'10'}
        Rooms.create_from_dict(d)
        d = {'department':'B', 'spots':'20'}
        Rooms.create_from_dict(d)
        d = {'department':'C', 'spots':'30'}
        Rooms.create_from_dict(d)

        response = self.csrf_client.get('/api/rooms/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertEqual(u'application/json',
            response._headers['content-type'][1])

        self.assertIn('"department": "A"', response.content.decode('utf-8'))
        self.assertIn('"department": "B"', response.content.decode('utf-8'))
        self.assertIn('"department": "C"', response.content.decode('utf-8'))
        self.assertNotIn('"department": "D"', response.content.decode('utf-8'))

        self.assertIn('"spots": 10', response.content.decode('utf-8'))
        self.assertIn('"spots": 20', response.content.decode('utf-8'))
        self.assertIn('"spots": 30', response.content.decode('utf-8'))
        self.assertNotIn('"spots": "10"', response.content.decode('utf-8'))

    def test_get_list_users(self):
        from xapp.models import tables
        from xapp.models import Users
        d = {'name':'A', 'paycheck':'10', 'date_joined': '2014-01-01'}
        Users.create_from_dict(d)
        d = {'name':'B', 'paycheck':'20', 'date_joined': '01/01/2014'}
        Users.create_from_dict(d)
        d = {'name':'C', 'paycheck':'30', 'date_joined': '02-01-2014'}
        Users.create_from_dict(d)

        response = self.csrf_client.get('/api/users/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertEqual(u'application/json',
            response._headers['content-type'][1])

        self.assertIn('"name": "A"', response.content.decode('utf-8'))
        self.assertIn('"name": "B"', response.content.decode('utf-8'))
        self.assertIn('"name": "C"', response.content.decode('utf-8'))
        self.assertNotIn('"department": "D"', response.content.decode('utf-8'))

        self.assertIn('"paycheck": 10', response.content.decode('utf-8'))
        self.assertIn('"paycheck": 20', response.content.decode('utf-8'))
        self.assertIn('"paycheck": 30', response.content.decode('utf-8'))
        self.assertNotIn('"paycheck": "10"', response.content.decode('utf-8'))

        self.assertNotIn('"date_joined": "2014/01/01"', response.content.decode('utf-8'))
        self.assertIn('"date_joined": "01/01/2014"', response.content.decode('utf-8'))
        self.assertIn('"date_joined": "02/01/2014"', response.content.decode('utf-8'))


    def test_delete_users(self):
        from xapp.models import tables
        from xapp.models import Users
        d = {'name':'A', 'paycheck':'10', 'date_joined': '2014-01-01'}
        Users.create_from_dict(d)
        d = {'name':'B', 'paycheck':'20', 'date_joined': '01/01/2014'}
        Users.create_from_dict(d)
        d = {'name':'C', 'paycheck':'30', 'date_joined': '02-01-2014'}
        Users.create_from_dict(d)
        response = self.csrf_client.delete('/api/users/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(405, response.status_code)
        self.assertEqual(u'application/json',
            response._headers['content-type'][1])


    def test_get_detail_users(self):
        from xapp.models import tables
        from xapp.models import Users
        d = {'name':'A', 'paycheck':'10', 'date_joined': '2014-01-01'}
        Users.create_from_dict(d)
        d = {'name':'B', 'paycheck':'20', 'date_joined': '01/01/2014'}
        Users.create_from_dict(d)
        d = {'name':'C', 'paycheck':'30', 'date_joined': '02-01-2014'}
        Users.create_from_dict(d)
        response = self.csrf_client.get('/api/users/1/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertEqual(u'application/json',
            response._headers['content-type'][1])
        self.assertIn('"name": "A"', response.content.decode('utf-8'))
        self.assertIn('"paycheck": 10', response.content.decode('utf-8'))
        self.assertIn('"date_joined": "01/01/2014"', response.content.decode('utf-8'))
        self.assertNotIn('"name": "B"', response.content.decode('utf-8'))


    def test_post_users(self):
        from xapp.models import tables
        from xapp.models import Users
        d = {'name':'A', 'paycheck':'10', 'date_joined': '2014-01-01'}
        Users.create_from_dict(d)
        d = {'name':'B', 'paycheck':'20', 'date_joined': '01/01/2014'}
        Users.create_from_dict(d)
        d = {'name':'C', 'paycheck':'30', 'date_joined': '02-01-2014'}
        Users.create_from_dict(d)
        response = self.csrf_client.post('/api/users/',
            {'name':'D', 'paycheck':'40', 'date_joined': '2014-01-04'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(201, response.status_code)
        self.assertEqual(u'application/json',
            response._headers['content-type'][1])
        self.assertIn('"name": "D"', response.content.decode('utf-8'))
        self.assertIn('"paycheck": 40', response.content.decode('utf-8'))
        self.assertIn('"date_joined": "04/01/2014"', response.content.decode('utf-8'))
        self.assertNotIn('"name": "A"', response.content.decode('utf-8'))

    def test_patch_users(self):
        from rest_framework.test import APIClient
        client = APIClient()
        from xapp.models import tables
        from xapp.models import Users
        d = {'name':'A', 'paycheck':'10', 'date_joined': '2014-01-01'}
        Users.create_from_dict(d)
        d = {'name':'B', 'paycheck':'20', 'date_joined': '01/01/2014'}
        Users.create_from_dict(d)
        d = {'name':'C', 'paycheck':'30', 'date_joined': '02-01-2014'}
        Users.create_from_dict(d)

        response = client.patch('/api/users/1/',
            {'name':'D'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        self.assertEqual(u'application/json',
            response._headers['content-type'][1])
        self.assertIn('"name": "D"', response.content.decode('utf-8'))
        self.assertIn('"paycheck": 10', response.content.decode('utf-8'))
        self.assertIn('"date_joined": "01/01/2014"', response.content.decode('utf-8'))
        self.assertNotIn('"name": "A"', response.content.decode('utf-8'))

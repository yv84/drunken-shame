#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os

from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.host = os.environ.get('HOST_TEST') or 'http://localhost:8000/'

    def tearDown(self):
        self.browser.quit()

    def test_admin_panel(self):
        admin_login = os.environ.get('ADMIN_LOGIN') or 'admin'
        admin_password = os.environ.get('ADMIN_PASSWORD') or 'admin'
        driver = self.browser.get(self.host+'admin/')
        self.browser \
            .find_element_by_css_selector("#id_username") \
            .send_keys(admin_login)
        self.browser \
            .find_element_by_css_selector("#id_password") \
            .send_keys(admin_password)
        self.browser.find_element_by_css_selector(".submit-row").submit()

        self.assertIn(u'Администрирование', self.browser.title)
        self.assertIn(u'Xapp',
            self.browser.find_element_by_css_selector(".app-xapp").text)
        self.assertIn(u'Комнаты',
            self.browser.find_element_by_css_selector(".app-xapp").text)
        self.assertIn(u'Пользователи',
            self.browser.find_element_by_css_selector(".app-xapp").text)


    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.host)

        self.assertIn(u'Web приложение', self.browser.title)
        #self.fail('Finish the test!')




if __name__ == '__main__':
    import sys
    if sys.version_info[0] == 2:
        import warnings
        with warnings.catch_warnings(record=True):
            unittest.main()
    elif sys.version_info[0] == 3:
        unittest.main(warnings='ignore')

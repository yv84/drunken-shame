#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import unittest


DEFAULT_WAIT = 5


class FunctionalTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.host = os.environ.get('HOST_TEST') or 'http://localhost:8000/'

    def tearDown(self):
        self.browser.quit()

    def wait_for(self, function_with_assertion, timeout=DEFAULT_WAIT):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                return function_with_assertion()
            except (AssertionError, WebDriverException):
                time.sleep(0.1)
        return function_with_assertion()


class NewVisitorTest(FunctionalTest):

    def setUp(self):
        super(NewVisitorTest, self).setUp()

    def tearDown(self):
        super(NewVisitorTest, self).tearDown()

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

    def test_home_page(self):
        driver = self.browser.get(self.host)
        self.assertIn(u'Web приложение', self.browser.title)
        self.assertTrue(
            u'Комнаты',
            self.browser \
                .find_element_by_css_selector("#sheet_name>div:nth-child(1)") \
                .text
        )
        self.assertTrue(
            u'Комнаты',
            self.browser \
                .find_element_by_css_selector("#sheet_name>div:nth-child(2)") \
                .text
        )


    def test_home_page_users(self):
        driver = self.browser.get(self.host)
        self.browser \
            .find_element_by_css_selector("#sheet_name>div:nth-child(1)") \
            .click()

        self.wait_for(
            lambda: self.assertEqual(
                u'Пользователи добавить:',
                self.browser \
                  .find_element_by_css_selector("#object_form>div>p") \
                  .text
            )
        )

        self.assertTrue(
            u'DataTables_Table_0_wrapper',
            self.browser \
              .find_element_by_css_selector("#sheet_field>div>div") \
              .get_attribute('id')
        )
        self.assertTrue(
            u'dataTables_wrapper no-footer',
            self.browser \
              .find_element_by_css_selector("#sheet_field>div>div") \
              .get_attribute('class')
        )
        self.assertTrue(
            u'Пользователи добавить:',
            self.browser \
              .find_element_by_css_selector("#object_form>div>p") \
              .text
        )


if __name__ == '__main__':
    import sys
    if sys.version_info[0] == 2:
        import warnings
        with warnings.catch_warnings(record=True):
            unittest.main()
    elif sys.version_info[0] == 3:
        unittest.main(warnings='ignore')

#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn(u'Web приложение', self.browser.title)
        self.fail('Finish the test!')


if __name__ == '__main__':
    import sys
    if sys.version_info[0] == 2:
        import warnings
        with warnings.catch_warnings(record=True):
            unittest.main()
    elif sys.version_info[0] == 3:
        unittest.main(warnings='ignore')

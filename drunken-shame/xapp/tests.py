from django.core.urlresolvers import resolve
from django.test import TestCase

# Create your tests here.

class SmokeTest(TestCase):

    def test_admin_url(self):
        found = resolve('/admin/')

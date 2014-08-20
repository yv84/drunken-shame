from django.core.urlresolvers import resolve
from django.test import TestCase

# Create your tests here.

class UrlsTest(TestCase):

    def test_login_url(self):
        found = resolve('/auth/login/')

    def test_signup_url(self):
        found = resolve('/auth/signup/')

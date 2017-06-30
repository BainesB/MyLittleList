from django.core.urlresolvers import resolve 
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page #2
from django.template.loader import render_to_string
'''
class SmokeTest(TestCase):
    
    def test_bad_maths(self):
            self.assertEqual(1 + 1, 3)
'''
class HomePageTest(TestCase):
    
    def test_uses_home_template(self):

        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

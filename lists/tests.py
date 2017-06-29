from django.core.urlresolvers import resolve 
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page #2

'''
class SmokeTest(TestCase):
    
    def test_bad_maths(self):
            self.assertEqual(1 + 1, 3)
'''
class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/') #1
        self.assertEqual(found.func, home_page) #1
            # this is checking that the root of the app '/' is the home_page
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()#1
        response = home_page(request)#2
        html = response.content.decode('utf8')#3
        self.assertTrue(html.startswith('<html>'))#4
        self.assertIn('<title>To-Do lists</title>', html)#5
        self.assertTrue(html.endswith('</html>'))#4

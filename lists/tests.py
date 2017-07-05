from django.core.urlresolvers import resolve 
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page #2
from django.template.loader import render_to_string
from django.db import models
from lists.models import Item
'''
class SmokeTest(TestCase):
    
    def test_bad_maths(self):
            self.assertEqual(1 + 1, 3)
'''

class HomePageTest(TestCase):
    
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

class ItemModelTest(TestCase):
    
    def test_saving_andretrieving_items(self):
        first_item = Item()
        first_item.text = 'The fist (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_item = Item.objects.all()
        self.assertEqual(saved_item.count(),2)

        first_saved_item = saved_item[0]
        second_saved_item = saved_item[1]
        self.assertEqual(first_saved_item.text, 'The fist (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

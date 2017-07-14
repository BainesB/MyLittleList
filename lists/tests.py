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
        self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(),1) #1
        new_item = Item.objects.first() #2
        self.assertEqual(new_item.text, 'A new list item') #3
    
    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text':'A new listitem'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_item_when_necessary(self):
            self.client.get('/')
            self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        
        response = self.client.get('/')
        
        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

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


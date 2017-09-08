# THIS IS MY VERSION

from django.core.urlresolvers import resolve 
from django.http import HttpRequest

from lists.views import home_page #2
from django.template.loader import render_to_string
from django.db import models

from django.test import TestCase
from lists.models import Item, List

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_item_when_necessary(self):

            self.client.get('/')
            self.assertEqual(Item.objects.count(), 0)
#	 	looks like it is checking the number of items on the page is 0
class ListAndItemModelsTest(TestCase):
#	this is checking the database    
    def test_saving_and_retrieving_items(self):
#	can we save and retrieve stuff.
        list_ = List()
#	setting list_ to an instance of TestCase.List()
        list_.save()
#	we are saving it. not sure where to?
        first_item = Item()
#	setting first_item to TestCase.Item()
        first_item.text = 'The first (ever) list item'
# 	setting first_item.text to a string. 
        first_item.list = list_
# 	setting first_item.list witch is TestCase.Item.list() to list_ which is a TestCase.list() ## this is baking the noodle. 
        first_item.save()
# 	save it somewhere. 

        second_item = Item()
# 	we are doing another item. 
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()
#	simply adding it in adition to the first item. 
        saved_list = List.objects.first()
# 	this is interesting. setting saved_list to the first item. 
        self.assertEqual(saved_list, list_)
#	checking that the first item and this current list (which only has one item) are not the same. 
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)
# 	check how much stuff is in the list. 
        first_saved_item = saved_items[0]
#	checking what the first saved item is. 
        second_saved_item = saved_items[1]	
#	checking what the second saved item is.
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
# 	checking the first item is what we think it should be. 
        self.assertEqual(first_saved_item.list, list_)
#	again. 
        self.assertEqual(second_saved_item.text, 'Item the second')
#	checking the second saved item is what we think it should be. 
        self.assertEqual(second_saved_item.list, list_)
#	list_ is List(). check that second_saved_item is list_. 
#	second_saved_item is the second thing in Item()
#       second_saved_item is saved_item[1] 
# 	save_items is Item.objects.all

class ListViewTest(TestCase):
# 	not sure what this is doing. 
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
# 	setting response to this url. 
#	f put a variable in to the url string. 
#	seems to be putting th list into the url. 
        self.assertTemplateUsed(response, 'list.html')
#	checking that the template used is list.html
    def test_displays_all_items(self):
        correct_list = List.objects.create()
#	setting correct_list to objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
#	create an object with the attribuet text set to 'itemey 1' and attribuetlist set to correct_list.
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')r
## what does this r at the end of the line do?         
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')
# make sure the other list items aren't going in the first list. 

class NewListTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(
            f'/lists/{correct_list.id}/add_item',

             data={'item_text': 'A new item for an existing list'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first() 
        self.assertEqual(new_item.text, 'A new item for an existing list') 
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):

        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item', 
            data={'item_text': 'A new item for an existing list'}
            )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')    

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text':'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response,f'/lists/{new_list.id}/')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

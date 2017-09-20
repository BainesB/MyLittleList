import os 
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver 
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time 

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase): 
	def setUp(self):
		self.browser = webdriver.Firefox()
		# setting browser to firefox
		staging_server = os.environ.get('STAGING_SERVER')
		if staging_server:
			self.live_server_url = 'http://' + staging_server

	def tearDown(self):
		self.browser.quit()
		# making a tearDown function. it just quits the browser. 

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		# setting start_time to the current time. 
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				# setting table to id_list_table. it is a forloop of the items in the db
				rows  = table.find_elements_by_tag_name('tr')
				#rows set to table-tr
				self.assertIn(row_text, [row.text for row in rows])
				# this is a counter and the text in each row
				return  
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e 
				time.sleep(0.5)
			# I think this breaks the loog out. 
 
	def test_can_start_a_list_for_one_user(self):
		self.browser.get(self.live_server_url)
		# this is gettng the url. 
		self.assertIn('To-Do', self.browser.title)
		# checking the browser title for To-do 
		header_text = self.browser.find_element_by_tag_name('h1').text 
		self.assertIn('To-Do', header_text)
		# checking h1 for To-Do 
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)
		# making inputbox form feild you enter text into
		inputbox.send_keys('Buy peacock feathers') 
		inputbox.send_keys(Keys.ENTER)  
		self.wait_for_row_in_list_table('1: Buy peacock feathers') 
		# seems to be using the function above so see if the input above went into the list table.		 
		inputbox = self.browser.find_element_by_id('id_new_item')

		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
		self.wait_for_row_in_list_table('1: Buy peacock feathers')


	def test_multiple_users_can_start_lists_at_different_urls(self):

		self.browser.get(self.live_server_url)

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+') 
		
		self.browser.quit()
		self.browser = webdriver.Firefox()

		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk') 
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk') # You have changed this.  from 2 / 1. 

		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)


		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

	def test_layout_and_styling(self):

		self.browser.get(self.live_server_url)
# 		get the lives server url. 
		self.browser.set_window_size(1024, 768) 
#		make the window a set size. 
		inputbox = self.browser.find_element_by_id('id_new_item')
# 		find id_new_item. set inputbox to it. 
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2, 
			512, 
			delta=215
		)
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512, 
			delta=215
		)

		

		self.fail('Finish the test!') 

from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        # The announcement the browser
        self.browser = webdriver.Firefox()

    def tearDown(self):
        # Close browser
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_list_for_one_user(self):
        # The announcement of page address
        self.browser.get(self.live_server_url)

        # Search for "Diary" word in the title
        self.assertIn("Diary", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Diary', header_text)

        # Enter some elements in list
        inputbox = self.browser.find_element_by_id('id_list_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            "Enter some cases"
        )

        # Writing some text in list
        inputbox.send_keys('Create online-shop')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Create online-shop')

        inputbox = self.browser.find_element_by_id('id_list_item')
        inputbox.send_keys('Upload on the internet')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('2: Upload on the internet')
        self.wait_for_row_in_list_table('1: Create online-shop')

    def test_multiple_users_can_start_list_at_different_url(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_list_item')
        inputbox.send_keys('Create online-shop')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Create online-shop')
        edith_list_url =self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        self.browser.quit()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Create online-shop',page_text)
        self.assertNotIn('Upload on the internet',page_text)

        inputbox = self.browser.find_element_by_id('id_list_item')
        inputbox.send_keys('Buy new book')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy new book')
        francis_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Create online-shop',page_text)
        self.assertNotIn('Buy new book',page_text)

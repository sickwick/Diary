from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        # The announcement the browser
        self.browser = webdriver.Firefox()

    def tearDown(self):
        # Close browser
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_list_and_retrieve_it_later(self):
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
        time.sleep(1)

        self.check_for_row_in_list_table('1: Create online-shop')

        inputbox = self.browser.find_element_by_id('id_list_item')
        inputbox.send_keys('Upload on the internet')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('2: Upload on the internet')
        self.check_for_row_in_list_table('1: Create online-shop')
        # Conclusion the test
        self.fail("Conclude the test")

from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        # The announcement the browser
        self.browser = webdriver.Firefox()

    def tearDown(self):
        # Close browser
        self.browser.quit()

    def test_can_start_list_and_retrieve_it_later(self):
        # The announcement of page address
        self.browser.get('http://localhost:8000')

        # Search for "Diary" word in the title
        self.assertIn("Diary", self.browser.title)
        self.fail("Conclude the test")


if __name__ == '__main__':
    unittest.main()

from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from .views import home_page


class HomePageTest(TestCase):
    def test_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf-8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Diary list</title>', html)
        self.assertTrue(html.endswith('</html>'))
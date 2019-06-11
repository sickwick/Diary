from django.test import TestCase

from .views import home_page
from .models import Item


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_a_post_request(self):
        response = self.client.post("/", data = {'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'lists/home.html')

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item=Item()
        first_item.text = "The first item ever"
        first_item.save()

        second_item=Item()
        second_item.text = "Second item"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item=saved_items[0]
        second_item_saved = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first item ever")
        self.assertEqual(second_item_saved.text, "Second item")
from django.test import TestCase

from .views import home_page
from .models import Item


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_a_post_request(self):
        response = self.client.post("/", data = {'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post("/", data = {'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')


    def test_save_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


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

    def test_display_all_list_items(self):
        Item.objects.create(text = 'item1')
        Item.objects.create(text = 'item2')

        responce = self.client.get('/')

        self.assertIn('item1', responce.content.decode())
        self.assertIn('item2', responce.content.decode())
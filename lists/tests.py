from django.test import TestCase

from .views import home_page
from .models import Item, List


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        responce = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(responce, 'lists/list.html')

    def test_display_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text = 'item1', list = correct_list)
        Item.objects.create(text = 'item2', list = correct_list)
        other_list = List.objects.create()
        Item.objects.create(text = 'other element from 1 list', list = other_list)
        Item.objects.create(text = 'other element from 2 list', list = other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')
        self.assertNotContains(response, "other element from 1 list")
        self.assertNotContains(response, "other element from 2 list")

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/')

        self.assertEqual(response.context['list'], correct_list)



class NewListTest(TestCase):

    def test_can_save_a_post_request(self):
        self.client.post("/lists/new", data = {'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data = {'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "The first item ever"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Second item"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_item_saved = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first item ever")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_item_saved.text, "Second item")
        self.assertEqual(second_item_saved.list, list_)

class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item', data = {'item_text':"A new item for list"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item', data = {'item_text':"A new item for list"})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

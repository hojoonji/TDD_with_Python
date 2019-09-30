from django.test import TestCase

from lists.models import Item, List

class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'home.html')

    def test_only_save_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='신규 작업 아이템 1', list=correct_list)
        Item.objects.create(text='신규 작업 아이템 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='다른 작업 아이템 1', list=other_list)
        Item.objects.create(text='다른 작업 아이템 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, '신규 작업 아이템 1')
        self.assertContains(response, '신규 작업 아이템 2')
        self.assertNotContains(response, '다른 작업 아이템 1')
        self.assertNotContains(response, '다른 작업 아이템 2')


class NewListTest(TestCase):
    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = '빈 아이템을 입력할 수 없습니다'
        self.assertContains(response, expected_error)


    def test_home_page_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={'item_text': '신규 작업 아이템'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "신규 작업 아이템")

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': '신규 작업 아이템'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item', data={'item_text': '기존 리스트에 새로운 아이템'} )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '기존 리스트에 새로운 아이템')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': '기존 리스트에 새로운 아이템'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)




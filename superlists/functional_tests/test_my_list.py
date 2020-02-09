from django.contrib.auth import get_user_model
from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage


User = get_user_model()

class MyListTest(FunctionalTest):


    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # edith는 logged in user다.
        self.create_pre_authenticated_session('edith@example.com')


        # 그녀는 홈페이지로 가서 리스트를 시작했다.
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Reticulate splines')
        list_page.add_list_item('Immanetize eschaton')
        first_list_url = self.browser.current_url

        # 그녀는 처음으로 "My lists" 링크를 알아챘다.
        self.browser.find_element_by_link_text('My lists').click()

        # 그녀는 그녀의 리스트가 첫번째 아이템의 이름을 따라 거기에 있는 걸 확인했다?
        self.wait_for(lambda: self.browser.find_element_by_link_text('Reticulate splines'))
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_list_url))

        # 그녀는 새로운 리스트를 시작하기로 했다.
        self.browser.get(self.live_server_url)

        list_page.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # "My lists" 밑에 새로운 리스트가 나타났다.

        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(lambda: self.browser.find_element_by_link_text('Click cows'))
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, second_list_url))

        # 그녀는 로그아웃했고 "My lists" 옵션은 사라졌다.
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.find_elements_by_link_text('My lists'),
                                     []))



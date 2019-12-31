from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

User = get_user_model()

class MyListTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_user, self.staging_pwd,
                                                   self.stating_port, self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        ## 쿠키를 설정하기 위해 임시 페이지를 방문한다. 아무 것도 없는 페이지로
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(name=settings.SESSION_COOKIE_NAME,
                                     value=session_key,
                                     path='/'))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # edith는 logged in user다.
        self.create_pre_authenticated_session('edith@example.com')

        # 그녀는 홈페이지로 가서 리스트를 시작했다.
        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanetize eschaton')
        first_list_url = self.browser.current_url

        # 그녀는 처음으로 "My lists" 링크를 알아챘다.
        self.browser.find_element_by_link_text('My lists').click()

        # 그녀는 그녀의 리스트가 첫번째 아이템의 이름을 따라 거기에 있는 걸 확인했다?
        self.wait_for(lambda: self.browser.find_element_by_link_text('Reticulate splines'))
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_list_url))

        # 그녀는 새로운 리스트를 시작하기로 했다.
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # "My lists" 밑에 새로운 리스트가 나타났다.
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(lambda: self.browser.find_element_by_link_text('Click cows'))
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, second_list_url))

        # 그녀는 로그아웃했고 "My lists" 옵션은 사라졌다.
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.find_element_by_link_text('My lists'),
                                     []))



from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage

from unittest import skip



def quit_if_possible(brower):
    try:
        brower.quit()
    except :
        pass


class SharingTest(FunctionalTest):

    @skip
    def test_can_share_a_list_with_another_user(self):
        # 에디스는 login 한 user다.
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # 그녀의 친구도 사이트에 접속했다.
        oni_browser = webdriver.Firefox()
        self.addCleanup(lambda : quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session('oni@example.com')

        # 에디스는 홈페이지로 가서 새로운 리스트를 시작한다
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Get help')

        # share this option이라는 버튼이 있는 것을 확인했다.
        share_box = list_page.get_share_box()
        self.assertEqual(share_box.get_attribute('placeholder'), 'your-friend@example.com')

        # 그녀는 그녀의 list를 공유한다.
        list_page.share_list_with('oni@example.com')







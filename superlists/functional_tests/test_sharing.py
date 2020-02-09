from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage

from unittest import skip



def quit_if_possible(brower):
    try:
        brower.quit()
    except :
        pass


class SharingTest(FunctionalTest):

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

        # oni는 자신의 브라우저로 list page로 간다
        self.browser = oni_browser
        MyListsPage(self).go_to_my_lists_page()

        # 그는 edith의 list를 찾을 수 있었다.
        self.browser.find_element_by_link_text('Get help').click()

        # oni는 이것이 edith의 페이지인 걸 알 수 있다.
        self.wait_for(lambda: self.assertEqual(list_page.get_list_owner(), 'edith@example.com'))

        # oni는 새로운 아이템을 추가했다.
        list_page.add_list_item('Hi Edith')

        # Edith가 화면을 refresh 했을 때 oni가 입력한 내용을 볼 수 있었다.
        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Hi Edith', 2)








from .base import FunctionalTest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .list_page import ListPage



class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_user(self):
        # 에디스(Edith)는 멋진 작업 목록 온라인 앱이 나왔다는 소식을 듣고
        # 해당 웹 사이트를 확인하러 간다.
        self.browser.get(self.live_server_url)

        # 웹 페이지 타이틀과 헤더가 'To-Do'를 표시하고 있다.
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('작업 목록 시작', header_text)

        list_page = ListPage(self)
        # 그녀는 바로 작업을 추가하기로 한다.
        inputbox = list_page.get_item_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'), '작업아이템입력')

        # "공작깃털 사기"라고 텍스트 상자에 입력한다.
        inputbox.send_keys("공작깃털 사기")

        # 엔터키를 치면 페이지가 갱신되고 작업 목록에
        # "1: 공작깃털 사기" 아이템이 추가된다.
        inputbox.send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table('공작깃털 사기', '1')

        # 추가 아이템을 입력할 수 있는 여분의 텍스트 상자가 존재한다.
        # 다시 "공작깃털을 이용해서 그물 만들기"라고 입력한다.
        inputbox = list_page.get_item_input_box()
        inputbox.send_keys('공작깃털을 이용해서 그물 만들기')
        inputbox.send_keys(Keys.ENTER)

        # 페이지는 다시 갱신되고, 두 개 아이템이 목록에 보인다.
        list_page.wait_for_row_in_list_table('공작깃털 사기', '1')
        list_page.wait_for_row_in_list_table('공작깃털을 이용해서 그물 만들기', '2')

        # 그녀는 만족한 채로 잠 자러 간다.

    def test_multiple_uesrs_can_start_lists_at_different_urls(self):
        list_page = ListPage(self)
        # 에디스는 새로운 작업 목록을 만든다.
        self.browser.get(self.live_server_url)
        self.browser.get(self.live_server_url)
        inputbox = list_page.get_item_input_box()
        inputbox.send_keys('공작깃털 사기')
        inputbox.send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table('공작깃털 사기', '1')

        # 그녀는 그녀의 리스트에 새로운 URL이 할당된 것을 확인했다.
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # 새로운 사용자인 프란시스가 사이트에 접속하다.

        ## 새로운 브라우저 세션을 이용해서 에디스의 정보가
        ## 쿠키를 통해 유입되는 것을 방지한다.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # 프란시스가 홈페이지에 접속한다.
        # 에디스의 리스트는 보이지 않는다.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertNotIn('공작길털을 이용해서 그물 만들기', page_text)

        # 프란시스가 새로운 작업 아이템을 입력한다.
        inputbox = list_page.get_item_input_box()
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table('우유 사기', '1')

        # 프란시스가 전용 URL을 취득한다.
        francis_url = self.browser.current_url
        self.assertRegex(francis_url, '/lists/.+')
        self.assertNotEqual(edith_list_url, francis_url)

        # 에디스가 입력한 흔적이 없다는 것을 다시 확인한다.
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertIn('우유 사기', page_text)

        # 둘 다 만족하고 잠자리에 든다.
            


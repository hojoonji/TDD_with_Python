from .base import FunctionalTest
from unittest import skip

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # 에디스는 홈페이지로 가서 실수로 빈 목록을 전송했다.
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 홈페이지는 리프레쉬 됐고 빈 아이템은 입력할 수 없다는 에러가 떴다.
        # 브라우저가 request를 인터셉트하고 리스트 페이지가 읽어들이지 않는다.
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))

        # 그녀는 이번에는 제대로 된 텍스트를 입력했고 제대로 작동했다. 
        # self.get_item_input_box().send_keys('우유 사기')
        self.add_list_item('우유 사기')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:valid'))
        # self.get_item_input_box().send_keys(Keys.ENTER)
        # self.wait_for_row_in_list_table('1: 우유 사기')

        # 그녀는 다시 빈 아이템을 입력해보기로 했다. 
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 그녀는 다시 비슷한 에러를 받았다.
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))

        # 그년 이번에는 제대로 입력하기로 했다.
        self.add_list_item('차 만들기')
        # self.get_item_input_box().send_keys('차 만들기')
        # self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 우유 사기')
        # self.wait_for_row_in_list_table('2: 차 만들기')

    def test_cannot_add_duplicate_items(self):
        # 에디스는 홈페이지로 가서 새로운 리스트를 시작한다.
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy wellies)')

        # 그녀는 실수로 똑같은 아이템을 입력했다.
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # 에러 메세지가 발생한 것을 확인했다.
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            '리스트에 같은 아이템이 이미 있습니다'
        ))

    def test_error_messages_are_cleared_on_input(self):
        # 에디스는 새로운 리스트를 시작하고 validation error 를 야기시켰다.
        self.browser.get(self.live_server_url)
        self.add_list_item('Banter too thick')

        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # 그녀는 에러를 클리어하기 위해 input box에 타이핑하기 시작했다.
        self.get_item_input_box().send_keys('a')

        # 그녀는 에러 메세지가 사라지는 걸 보았다.
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))





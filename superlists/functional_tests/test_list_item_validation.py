from .base import FunctionalTest
from unittest import skip

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # 에디스는 홈페이지로 가서 실수로 빈 목록을 전송했다.
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # 홈페이지는 리프레쉬 됐고 빈 아이템은 입력할 수 없다는 에러가 떴다.
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "빈 아이템을 입력할 수 없습니다"
            ) 
        )

        # 그녀는 이번에는 제대로 된 텍스트를 입력했고 제대로 작동했다. 
        self.browser.find_element_by_id('id_new_item').send_keys('우유 사기')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 우유 사기')

        # 그녀는 다시 빈 아이템을 입력해보기로 했다. 
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # 그녀는 다시 비슷한 에러를 받았다.
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "빈 아이템을 입력할 수 없습니다"
            ) 
        )

        # 그년 이번에는 제대로 입력하기로 했다.
        self.browser.find_element_by_id('id_new_item').send_keys('차 만들기')
        self.wait_for_row_in_list_table('1: 우유 사기')
        self.wait_for_row_in_list_table('2: 차 만들기')







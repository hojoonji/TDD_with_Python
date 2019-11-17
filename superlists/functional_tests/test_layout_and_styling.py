import os 
from .base import FunctionalTest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        if os.environ.get('OS_TYPE'):
            return

        # 에디스는 홈페이지로 간다.
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # 화면에 입력박스가 가운데에 위치하고 있다.
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

        # 그녀는 새로운 리스트를 시작했고 역시나 가운데 정렬이 된 입력상자를 보았다.
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')

        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

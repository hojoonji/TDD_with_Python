from .base import FunctionalTest
from unittest import skip

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # 에디스는 홈페이지로 가서 실수로 빈 목록을 전송했다.
        # 홈페이지는 리프레쉬 돘고 빈 아이템은 입력할 수 없다는 에러가 떴다.
        # 그녀는 이번에는 제대로 된 텍스트를 입력했고 제대로 작동했다. 

        # 그녀는 다시 빈 아이템을 입력해보기로 했다. 
        # 그녀는 다시 비슷한 에러를 받았다.
        self.fail('write me')







import time
import os
from pyvirtualdisplay import Display
from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


MAX_WAIT = 10

class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        os_type = os.environ.get('OS_TYPE')
        print(f'os_type in: {os_type}')
        if  os_type:
            cls.display = Display(visible=0, size=(800,600))
            cls.display.start()

        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            print(f"staging server is : {staging_server}")
            cls.live_server_url = 'http://' + staging_server
        else:
            print(f"no staging server:{cls.live_server_url}")

    @classmethod
    def tearDownClass(cls):
        os_type = os.environ.get('OS_TYPE')
        print(f'os_type out: {os_type}')
        if  os_type:
            cls.display.stop()

    def setUp(self): 
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn() 
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')


import time
import os
from pyvirtualdisplay import Display

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from .server_tools import reset_database

MAX_WAIT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        os_type = os.environ.get('OS_TYPE')
        print(f'os_type in: {os_type}')
        if os_type:
            cls.display = Display(visible=0, size=(800,600))
            cls.display.start()

        cls.staging_server = os.environ.get('STAGING_SERVER')
        cls.staging_user = os.environ.get('STAGING_USER')
        cls.staging_pwd = os.environ.get('STAGING_PWD')
        cls.stating_port = os.environ.get('STAGING_PORT')

        if cls.staging_server:
            print(f"staging server is : {cls.staging_server}")
            cls.live_server_url = 'http://' + cls.staging_server
            reset_database(cls.staging_user, cls.staging_pwd, cls.staging_server, cls.stating_port)
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


    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)



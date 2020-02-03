import time
import os
from pyvirtualdisplay import Display
from datetime import datetime

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from .server_tools import reset_database

from .management.commands.create_session import  create_pre_authenticated_session
from .server_tools import create_session_on_server

MAX_WAIT = 10
SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'screendumps')


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
        if os_type:
            cls.display.stop()


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


    def setUp(self): 
        self.browser = webdriver.Firefox()
        super().setUp()

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()

        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        return any(error for (method, error) in self._outcome.errors)

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to ' + filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to ' + filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )

    @wait
    def wait_for(self, fn):
        return fn()


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



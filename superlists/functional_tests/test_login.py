from django.core import  mail
from selenium.webdriver.common.keys import Keys
import re
from .base import FunctionalTest

TEST_EMAIL='hj@toss.im'
SUBJECT='Your login link for superlists'

class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        #에디스는 홈페이지에 가서 "Log in" 섹션이 navbar에 있는 걸 확인했다.
        #그녀는 이메일 주소를 입력해보기로 했다.
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # 이메일이 보내졌다는 메시지가 나타났다.
        self.wait_for(lambda: self.assertIn('Check your email', self.browser.find_element_by_tag_name('body').text))

        # 그녀는 이메일을 확인했고 새로운 메일이 도착한 것을 확인했다.
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(SUBJECT, email.subject)

        # 메일에 url link가 있었다.
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # 그녀는 url을 클릭했다.
        self.browser.get(url)
        
        # 그녀는 로그인에 성공했다.
        self.wait_for(lambda: self.browser.find_element_by_link_text('Log out'))
        
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)



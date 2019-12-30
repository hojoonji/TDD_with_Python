from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
import os
import poplib
import time
from .base import FunctionalTest

SUBJECT='Your login link for Superlists'

class LoginTest(FunctionalTest):
    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body
        
        email_id = None
        time.sleep(3)
        start = time.time()
        inbox = poplib.POP3_SSL('pop.gmail.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['GMAIL_PASSWORD'])
            while time.time() - start < 60:
                # 최근 10개의 메일을 가져온다.
                count, _ = inbox.stat()
                # for i in range(max(1, count - 10), count+1):
                for i in reversed(range(max(1, count - 10), count+1)):
                    print('getting msg', i)
                    _, lines, _ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    # print(lines)
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = "\n".join(lines)
                        if email_id:
                            inbox.dele(email_id)
                        return body
                time.sleep(5)
        finally:
            inbox.quit()

    def test_can_get_email_link_to_log_in(self):
        #에디스는 홈페이지에 가서 "Log in" 섹션이 navbar에 있는 걸 확인했다.
        #그녀는 이메일 주소를 입력해보기로 했다.
        if self.staging_server:
            test_email = 'sleepernewsnews@gmail.com'
        else:
            test_email = 'edith@example.com'

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # 이메일이 보내졌다는 메시지가 나타났다.
        self.wait_for(lambda: self.assertIn('Check your email', self.browser.find_element_by_tag_name('body').text))

        # 그녀는 이메일을 확인했고 새로운 메일이 도착한 것을 확인했다.
        body = self.wait_for_email(test_email, SUBJECT)

        # 메일에 url link가 있었다.
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)

        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # 그녀는 url을 클릭했다.
        self.browser.get(url)
        
        # 그녀는 로그인에 성공했다.
        self.wait_to_be_logged_in(email=test_email)

        # 이제 로그아웃 한다.
        self.browser.find_element_by_link_text('Log out').click()

        # 로그 아웃 됐다.
        self.wait_to_be_logged_out(email=test_email)




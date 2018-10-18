from django.test import TestCase, Client
from wechat.models import User, Activity
import json
from django.utils import timezone
import xml.etree.ElementTree as ET

test_user_openid = ['1111', '2222']
test_student_id = [2016018485, 2016016666]

ticket_unique_id = 'fff'

XML_TEXT_BASE = """
<xml>
 <ToUserName><![CDATA[aaabbb]]></ToUserName>
 <FromUserName><![CDATA[%s]]></FromUserName>
 <CreateTime>1460536575</CreateTime>
 <MsgType>text</MsgType>
 <MsgId>6272956824639273066</MsgId>
 <Content><![CDATA[%s]]></Content>
</xml>"""

reply_data = '<![CDATA[%s]]>'

published_activity = Activity(id=3, name='published', key='key', place='place',
                              description='description', start_time=timezone.now(), pic_url="pic_url",
                              end_time=timezone.now(), book_start=timezone.now(), book_end=timezone.now(),
                              total_tickets=1, status=Activity.STATUS_PUBLISHED, remain_tickets=1)

class TicketOperationTestCase(TestCase):
    """
    Test user bind
    """
    def setUp(self):
        # if you visit in wechat, will do the following things
        user_len = len(test_user_openid)
        for i in range(user_len):
            User(open_id=test_user_openid[i], student_id=test_student_id[i]).save()
        self.c = Client()
        published_activity.save()
        self.get_key_text = [XML_TEXT_BASE % (test_user_openid[i], '抢票 key') for i in range(user_len)]
        self.refund_key_text = [XML_TEXT_BASE % (test_user_openid[i], '退票 key') for i in range(user_len)]
        self.show_key_text = [XML_TEXT_BASE % (test_user_openid[i], '取票 key') for i in range(user_len)]

    def tearDown(self):
        User.objects.get(open_id=test_user_openid).delete()
        Activity.objects.get(id=3).delete()

    def test_ticket(self):
        def test_get(send_data, result):
            response = self.c.post('/wechat', send_data)
            response_str = response.content.decode('utf-8')
            root = ET.fromstring(response_str)
            self.assertEqual(root.find('Content').text, reply_data % result)

        test_get(self.get_key_text, '抢票成功')

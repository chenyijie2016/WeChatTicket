from django.test import TestCase, Client
from wechat.models import User, Activity, Ticket
import json
from django.utils import timezone

deleted_activity = Activity(id=1, name='deleted', key='key', place='place',
                            description='description', start_time=timezone.now(), pic_url="pic_url",
                            end_time=timezone.now(), book_start=timezone.now(), book_end=timezone.now(),
                            total_tickets=100, status=Activity.STATUS_DELETED, remain_tickets=100)

saved_activity = Activity(id=2, name='saved', key='key', place='place',
                          description='description', start_time=timezone.now(), pic_url="pic_url",
                          end_time=timezone.now(), book_start=timezone.now(), book_end=timezone.now(),
                          total_tickets=100, status=Activity.STATUS_SAVED, remain_tickets=100)

published_activity = Activity(id=3, name='published', key='key', place='place',
                              description='description', start_time=timezone.now(), pic_url="pic_url",
                              end_time=timezone.now(), book_start=timezone.now(), book_end=timezone.now(),
                              total_tickets=100, status=Activity.STATUS_PUBLISHED, remain_tickets=100)

# Create your tests here.
class ActivityGetTestCase(TestCase):
    """
    Test user bind
    """
    def setUp(self):
        deleted_activity.save()
        saved_activity.save()
        published_activity.save()

    def tearDown(self):
        Activity.objects.get(id=1).delete()
        Activity.objects.get(id=2).delete()
        Activity.objects.get(id=3).delete()

    def test_notavailable_activity_get(self):
        c = Client()
        response = c.get('/api/u/activity/detail?id=1')
        response_str = response.content.decode('utf-8')
        response_dict = json.loads(response_str)
        self.assertNotEqual(response_dict['code'], 0)
        response = c.get('/api/u/activity/detail?id=2')
        response_str = response.content.decode('utf-8')
        response_dict = json.loads(response_str)
        self.assertNotEqual(response_dict['code'], 0)

    def test_activity_get(self):
        c = Client()
        response = c.get('/api/u/activity/detail?id=3')
        response_str = response.content.decode('utf-8')
        response_dict = json.loads(response_str)
        self.assertEqual(response_dict['code'], 0)
        response_dict = response_dict['data']
        self.assertEqual(response_dict['name'], 'published')
        self.assertEqual(response_dict['bookStart'], int(published_activity.book_start.timestamp()))
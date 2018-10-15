from django.test import TestCase, Client
from django.contrib.auth.models import User

from adminpage.views.activity import *
from wechat.models import Activity, Ticket
from codex.baseerror import *

# Create your tests here.


class ImageUploadTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username = 'amdin', email = 'admin@test.com', password = 'admin_psw')
        
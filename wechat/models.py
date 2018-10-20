from django.db import models

from codex.baseerror import LogicError
from WeChatTicket.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET


class User(models.Model):
    open_id = models.CharField(max_length=64, unique=True, db_index=True)
    student_id = models.CharField(max_length=32, db_index=True)

    # Cancel unique to fix bug when two default student with student_id=''

    @classmethod
    def get_by_openid(cls, openid):
        try:
            return cls.objects.get(open_id=openid)
        except cls.DoesNotExist:
            raise LogicError('User not found')


class Activity(models.Model):
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=64, db_index=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    place = models.CharField(max_length=256)
    book_start = models.DateTimeField(db_index=True)
    book_end = models.DateTimeField(db_index=True)
    total_tickets = models.IntegerField()
    status = models.IntegerField()
    pic_url = models.CharField(max_length=256)
    remain_tickets = models.IntegerField()

    STATUS_DELETED = -1
    STATUS_SAVED = 0
    STATUS_PUBLISHED = 1

    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.objects.filter(status=cls.STATUS_PUBLISHED).get(id=id)
        except cls.DoesNotExist:
            raise LogicError('Activity not found')


class Ticket(models.Model):
    student_id = models.CharField(max_length=32, db_index=True)
    unique_id = models.CharField(max_length=64, unique=True)
    # activity = models.ForeignKey(Activity)
    activity_id = models.IntegerField()
    status = models.IntegerField()

    STATUS_CANCELLED = 0
    STATUS_VALID = 1
    STATUS_USED = 2

    @classmethod
    def get_student_ticket(cls, openid, ticket):
        try:
            return cls.objects.filter(student_id=User.get_by_openid(openid).student_id).get(unique_id=ticket)
        except cls.DoesNotExist:
            raise LogicError('Ticket owned by the owner not found')


class MenuIdList():
    updated = False
    menus = []

    @classmethod
    def get_menu(cls):
        from wechat.wrapper import WeChatLib
        if cls.updated:
            return cls.menus
        current_menu = WeChatLib(WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET).get_wechat_menu()
        existed_button = list()
        for btn in current_menu:
            if btn['name'] == '抢票':
                existed_button += btn.get('sub_button', list())
        activity_ids = list()
        for btn in existed_button:
            if 'key' in btn:
                activity_id = btn['key']
                if activity_id.startswith('BOOKING_ACTIVITY_'):
                    activity_id = activity_id[len('BOOKING_ACTIVITY_')]
                if activity_id and activity_id.isdigit():
                    activity_ids.append(int(activity_id))
        cls.menus = activity_ids
        cls.updated = True
        return cls.menus

    @classmethod
    def set_menu(cls, new_menu):
        cls.updated = False
        cls.menus = new_menu
        cls.updated = True

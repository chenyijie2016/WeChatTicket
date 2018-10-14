from codex.baseerror import *
from codex.baseview import APIView

from wechat.models import Activity
from wechat.models import Ticket
from adminpage.serializers import activitySerializer
from django.conf import settings

import os
import time


class ActivityList(APIView):

    def get(self):

        if not self.request.user.is_authenticated():
            raise ValidateError("not login")

        activity_set = Activity.objects.exclude(status = Activity.STATUS_DELETED)
        activity_list = []
        for activity in activity_set:
            activity_serial = activitySerializer(activity)
            activity_list.append(activity_serial)

        return activity_list


class ActivityDelete(APIView):

    def post(self):
        self.check_input('id')
        try:
            activity_to_del = Activity.objects.get(id=self.input['id'])
        except Activity.DoesNotExist:
            raise DatabaseError("activity with id %d does not exist", self.input['id'])
        if activity_to_del.status == Activity.STATUS_DELETED:
            raise LogicError("activity with id %d deleted twice", self.input['id'])
        activity_to_del.status = Activity.STATUS_DELETED
        activity_to_del.save()


class ActivityCreate(APIView):

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("not login")

        self.check_input('name', 'key', 'place', 'picUrl', 'startTime',
                         'endTime', 'bookStart', 'bookEnd', 'totalTickets', 'status')
        try:
            Activity.objects.create(name = self.input['name'],
                                    key = self.input['key'],
                                    place = self.input['place'],
                                    description = self.input['description'],
                                    start_time = self.input['startTime'],
                                    pic_url = self.input['picUrl'],
                                    end_time = self.input['endTime'],
                                    book_start = self.input['bookStart'],
                                    book_end = self.input['bookEnd'],
                                    total_tickets = self.input['totalTickets'],
                                    status = self.input['status'],
                                    remain_tickets = self.input['totalTickets'])
        except Exception as e:
            raise DatabaseError('create admin with name %s failed' % self.input['name'])

class ImageUpload(APIView):

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("not login")

        img = self.input['image']
        img_path = os.path.join(settings.IMAGE_ROOT, img.name)
        try:
            with open(img_path, 'wb') as imgp:
                for info in img.chunks():
                    imgp.write(info)
            img_url = 'https://' + '635149.iterator-traits.com' + '/img/' + img.name
            return img_url
        except Exception as e:
            raise FileError("upload file with name %s failed" % img.name)


class ActivityDetail(APIView):

    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("not login")
        try:
            activity = Activity.objects.get(id = self.input['id'])
            activity_detail = {}
            activity_detail['name'] = activity.name
            activity_detail['key'] = activity.key
            activity_detail['description'] = activity.description
            activity_detail['startTime'] = activity.start_time.timestamp()
            activity_detail['endTime'] = activity.end_time.timestamp()
            activity_detail['place'] = activity.place
            activity_detail['bookStart'] = activity.book_start.timestamp()
            activity_detail['bookEnd'] = activity.book_end.timestamp()
            activity_detail['totalTickets'] = activity.total_tickets
            activity_detail['picUrl'] = activity.pic_url
            activity_detail['bookedTickets'] = activity.total_tickets - activity.remain_tickets
            activity_detail['usedTickets'] = Ticket.objects.count(status = Ticket.STATUS_USED)
            activity_detail['currentTime'] = time.time()
            activity_detail['status'] = activity.status

            return activity_detail

        except Exception as e:
            raise DatabaseError("get detail with id %d failed" % self.input['id'])

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("not login")

        self.check_input('id', 'name', 'description', 'picUrl', 'startTime', 'endTime', 'bookStart', 'bookend',
                         'totalTickets', 'status')

        try:
            activity = Activity.objects.get(id = self.input['id'])
            activity_status = activity.status
            current_time = time.time()

            activity.description = self.input['description']
            activity.pic_url = self.input['picUrl']
            if activity_status == Activity.STATUS_SAVED:
                activity.name = self.input['name']
                activity.place = self.input['place']
                activity.book_start = self.input['bookStart']
                activity.status = self.input['status']

            if current_time < activity.book_start:
                activity.total_tickets = self.input['totalTickets']

            if current_time < activity.start_time:
                activity.book_end = self.input['bookEnd']


            if current_time < activity.end_time:
                activity.start_time = self.input['startTime']
                activity.end_time = self.input['endTime']
        except Exception as e:
            raise DatabaseError('change detailed with id %d failed' % self.input['id'])



class ActivityMenu(APIView):
    def get(self):

        if not self.request.user.is_authenticated():
            raise LogicError("not login")

        activity_set = Activity.objects.filter(status = Activity.STATUS_PUBLISHED)
        activity_list = []
        for activity in activity_set:
            menu_item = {'id': activity.id, 'name': activity.name, 'menuIndex': activity.indexes}
            activity_list.append(menu_item)
        return activity_list

    def post(self):
        pass

class ActivityCheckin(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("not login")
        self.check_input('actId')
        try:
            activity = Activity.objects.get(id = self.input['id'])
            if 'ticket' in self.input:
                ticket = Ticket.objects.get(unique_id = self.input['ticket'])
            else:
                ticket = Ticket.objects.get(student_id = self.input['studentId'])
        except Exception as e:
            raise DatabaseError("get activity or ticket failed")

        if ticket.activity.id == activity.id:
            data = {'ticket': ticket.unique_id, 'studentId': ticket.student_id}
            return data
        else:
            raise TicketError("check ticket with id %d failed" % ticket.unique_id)
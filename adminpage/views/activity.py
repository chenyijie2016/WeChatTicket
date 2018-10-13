from codex.baseerror import *
from codex.baseview import APIView

from wechat.models import Activity
from adminpage.serializers import activitySerializer


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

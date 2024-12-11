from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import datetime
import pytz

class MyCustomAuthBackend(BaseBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        MyUser = get_user_model()
        try:
            my_user = MyUser.objects.get(username=username)
            if my_user.check_password(password):
                current_time = now().astimezone(pytz.timezone('UTC')).time()
                time_allowed = my_user.allowed_time_ranges
                start_time = self.convert_to_time(time_allowed.get('start'))
                end_time = self.convert_to_time(time_allowed.get('end'))

                if start_time <= current_time <= end_time:
                    return my_user
        except MyUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        MyUser = get_user_model()
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None

    def convert_to_time(self, time_str):
        return datetime.strptime(time_str, '%H:%M').time()

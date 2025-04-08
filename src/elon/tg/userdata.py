
from elon.users.models import Log

class UserLog:
    def __init__(self, tg_id):
        self.tg_id = tg_id
        self.log = Log.objects.filter(user_id=tg_id).first()
        if not self.log:
            self.log = Log.objects.create(user_id=tg_id, messages={'state': 0, 'menu_state': 0})

    def get_log(self):
        message = self.log.messages
        return message

    def change_log(self, message):
        self.log.messages = message
        self.log.save()

    def clear_log(self, state=0):
        self.log.messages = {'state': state, 'menu_state': 0}
        self.log.save()
class ServiceStatus:
    NOT_ACTIVE = 1
    ACTIVE = 2
    MODERATION = 3

    CHOICES = [
        (NOT_ACTIVE, "Aktiv emas"),
        (MODERATION, "Moderatsiya"),
        (ACTIVE, "Aktiv"),
    ]

    @classmethod
    def getValue(self, index):
        result = '-'
        for i, name in self.CHOICES:
            if i == index:
                result = name
        return result

STATUS_PAYMENT = (
                  (0, 'Not process'),
                  (1, 'CREATED'),
                  (2, 'COMPLETED'),
                  (-1, 'CANCELLED'),
                  (-2, 'CANCELLED_AFTER_COMPLETE')
                  )
class Status:
    NOT_PROCESS = 0
    CREATED = 1
    COMPLETED = 1
    CANCELLED = -1
    CANCELLED_AFTER_COMPLETE = -2

    CHOICES = [
        (NOT_PROCESS, "Not process"),
        (CREATED, "CREATED"),
        (COMPLETED, "COMPLETED"),
        (CANCELLED, "CANCELLED"),
        (CANCELLED_AFTER_COMPLETE, "CANCELLED_AFTER_COMPLETE"),
    ]

    @classmethod
    def getValue(self, index):
        result = '-'
        for i, name in self.CHOICES:
            if i == index:
                result = name
        return result


def default_title():
    return {
        "title_ru": "",
        "title_uz": ""
    }


def default_services():
    return {
        "top": 0,
        "auto_post": 0 
    }

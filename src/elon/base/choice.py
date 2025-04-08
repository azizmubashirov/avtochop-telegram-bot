class Gender:
    MEN = 1
    WOMEN = 2
    CHOICES = [
        (
            MEN,
            'Муж.',
        ),
        (
            WOMEN,
            'Жен.'
        )
    ]
    @classmethod
    def getValue(self, index):
        result = 'No'
        for i, name in self.CHOICES:
            if i == index:
                result = name
        return result

class ActiveStatus:
    NOT_ACTIVE = 0
    ACTIVE = 1
    DELETED = -1

    CHOICES = [
        (
            NOT_ACTIVE,
            'Неактивный ',
        ),
        (
            ACTIVE,
            'Активный '
        ),
        (
            DELETED,
            'Удалено'
        )
    ]
    @classmethod
    def getValue(self, index):
        result = 'No'
        for i, name in self.CHOICES:
            if i == index:
                result = name
        return result

from django.db import models
from django.utils import timezone
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.fields import VersatileImageField, PPOIField

class File(models.Model):
    file = VersatileImageField(upload_to="files/",
                               blank=False,
                               null=False,
                               width_field='width',
                               height_field='height',
                               ppoi_field='ppoi'
                               )
    height = models.PositiveIntegerField(
        'Image Height',
        blank=True,
        null=True
    )
    width = models.PositiveIntegerField(
        'Image Width',
        blank=True,
        null=True
    )
    ppoi = PPOIField(
        'Image PPOI'
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.file.name

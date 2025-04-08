from django.db import models
from elon.geo.utils import create_name_slug


class Region(models.Model):
    id = models.AutoField(primary_key=True, null=False, )
    name_uz = models.CharField(max_length=100, verbose_name="uz name")
    name_ru = models.CharField(max_length=100, verbose_name="ru name")
    ordering = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, max_length=255, allow_unicode=True, null=True)

    def __unicode__(self):
        return self.name_uz

    def __str__(self):
        return self.name_uz

    def save(self, *args, **kwargs):
        self.slug = create_name_slug(self)
        return super().save(*args, **kwargs)


class District(models.Model):
    id = models.AutoField(primary_key=True, null=False, )
    name_uz = models.CharField(max_length=100, verbose_name="uz name")
    name_ru = models.CharField(max_length=100, verbose_name="ru name")
    region = models.ForeignKey(Region, related_name="district_region", on_delete=models.CASCADE)
    ordering = models.PositiveIntegerField(default=0)

    @property
    def parent(self):
        return self.region

    def __unicode__(self):
        return self.name_uz

    def __str__(self):
        return self.name_uz

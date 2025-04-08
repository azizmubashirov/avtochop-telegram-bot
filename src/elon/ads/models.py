
from django.db import models
from elon.users.models import User
from elon.eav.models import Category, Marka, Model, Positsion
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from elon.geo.models import Region, District
from elon.payment.models import Service
from elon.ads.utils import create_title_slug

def default_title():
    return {
        "title_uz": "",
        "title_ru": ""
    }

def default_contact():
    return {
        "phone_number": ""
    }

def default_properties():
    return {}

def default_is_price():
    return {}

def default_search():
    return {}


class Ad(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    slug = models.SlugField(unique=True, max_length=355, allow_unicode=True, null=True, blank=True)
    description = models.TextField(blank=False, null=False)
    user = models.ForeignKey(User, related_name="ad_user", blank=False, null=True, on_delete=models.SET_NULL)
    images = ArrayField(models.URLField(blank=True, null=True, max_length=500), size=10, blank=True, null=True)
    reduced_images = ArrayField(models.URLField(blank=True, null=True, max_length=500), size=10, blank=True, null=True)
    category = models.ForeignKey(Category, related_name="ad_category", blank=False, null=True, on_delete=models.SET_NULL)
    prices = models.JSONField(blank=True, null=True, default=default_is_price)
    properties = models.JSONField(blank=True, null=True, default=default_properties)
    contact = models.JSONField(blank=False, null=False, default=default_contact)
    region = models.ForeignKey(Region, related_name="ads_region", blank=False, null=True, on_delete=models.SET_NULL)
    district = models.ForeignKey(District, related_name="ads_district", blank=True, null=True,
                                 on_delete=models.SET_NULL)
    type = models.IntegerField(choices=[(1, "Sale"), (2, "Removable")], blank=True, null=True)
    torg = models.IntegerField(choices=[(1, "Bor"), (2, "Yoq")], blank=True, null=True)
    status = models.IntegerField(
        choices=[(1, "Moderating"), (2, "Refused"), (3, "Submitted"), (4, "Active"), (5, "Inactive"),
                 (6, "Deactivated")],
        default=1, blank=False, null=False
    )
    moderator = models.ForeignKey(User, related_name="ad_moderator", blank=True, null=True, on_delete=models.SET_NULL)
    moderated = models.DateTimeField(blank=True, null=True)  # dashboard edit

    views_count = models.BigIntegerField(blank=False, null=False, default=0)
    favourite_count = models.BigIntegerField(blank=False, null=False, default=0)
    call_count = models.BigIntegerField(blank=False, null=False, default=0)
    currency = models.PositiveIntegerField(blank=True, null=True, choices=[(1, "so'm"), (2, "y.e")])

    created_by = models.ForeignKey(User, related_name="ad_created_by", blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now, editable=False)  # dashboard create, telegram bot

    updated_by = models.ForeignKey(User, related_name="ad_updated_by", blank=True, null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(blank=True, null=True)  # dashboard edit

    deleted_by = models.ForeignKey(User, related_name="ad_deleted_by", blank=True, null=True, on_delete=models.SET_NULL)
    deleted_at = models.DateTimeField(blank=True, null=True)  # dashboard delete

    marka = models.ForeignKey(Marka, related_name="ad_marka", blank=True, null=True, on_delete=models.SET_NULL)
    model = models.ForeignKey(Model, related_name="ad_madel", blank=True, null=True, on_delete=models.SET_NULL)
    positsion = models.ForeignKey(Positsion, related_name="ad_positsion", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = create_title_slug(self)
        return super().save(*args, **kwargs)

class AdFavourite(models.Model):
    ad = models.ForeignKey(Ad, related_name="favourite_ad", blank=False, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="favourite_ad_user", blank=False, null=False, on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=1, blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        unique_together = ("ad", "user")


class AdComment(models.Model):
    ad = models.ForeignKey(Ad, related_name="ad_comment", blank=True, null=True, on_delete=models.SET_NULL)
    comment = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"{self.ad.id} - {self.comment}"

class CategoryService(models.Model):
    category = models.ForeignKey(Category, related_name="cs_category", blank=False, null=True,
                                 on_delete=models.SET_NULL)
    service = models.ForeignKey(Service, related_name="cs_service", blank=False, null=True, on_delete=models.SET_NULL)
    limit = models.PositiveIntegerField(blank=True, null=False, default=0)
    price = models.PositiveIntegerField(blank=True, null=False, default=0)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        unique_together = ("category", "service")

        
class AdFilter(models.Model):
    category = models.ForeignKey(Category, related_name="category_id", blank=False, null=True, on_delete=models.SET_NULL)
    properties = ArrayField(models.CharField(blank=False, null=False, max_length=300), size=10, blank=True, null=True)
    
    class Meta:
        unique_together = ("category", "properties")

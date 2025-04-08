from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from django.utils.text import slugify
from elon.eav.utils import create_title_slug, create_label_slug, create_attribute_slug, create_input_title_slug


def default_title():
    return {
        "title_uz": "",
        "title_ru": "",
    }

def default_title_auto():
    return {
    }


def default_title_web():
    return {
    }


def default_seo_title():
    return {
        "seo_title_uz": "",
        "seo_title_ru": ""
    }


def default_seo_desc():
    return {
        "seo_desc_uz": "",
        "seo_desc_ru": ""
    }


def default_label():
    return {
        "label_uz": "",
        "label_ru": ""
    }


def default_config():
    return {
        "show_label": True
    }


def default_properties():
    return {
        "dataType": "",
        "label": {
            "label_uz": "",
            "label_ru": ""
        },
        "help": {
            "help_uz": "",
            "help_ru": ""
        },
        "values": [
            {
                "value": "",
                "label": "",
                "parent_id": ""
            },
        ],
        "validation": {
            "rule": "",
            "min": 0,
            "max": 0,
            "message": {
                "message_uz": "",
                "message_ru": ""
            }
        },
        "unit": {
            "unit_uz": "",
            "unit_ru": "",
        },
        "multiple": False,
        "filter": False
    }


class Category(MPTTModel):
    title = models.JSONField(default=default_title)
    seo_title = models.JSONField(default=default_seo_title, blank=True, null=False)
    seo_desc = models.JSONField(default=default_seo_desc, blank=True, null=False)
    image = models.ImageField(upload_to='category', null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    slug = models.SlugField(unique=True, max_length=255, allow_unicode=True)
    sorting = models.PositiveIntegerField(blank=True, null=True)
    click_count = models.BigIntegerField(blank=False, null=False, default=0)
    ads_count = models.BigIntegerField(blank=False, null=False, default=0)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    marka = models.CharField(max_length=255, blank=True, null=True)

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['mptt_level']

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = create_title_slug(self)
        return super().save(*args, **kwargs)

class InputType(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False, unique=True)
    slug = models.SlugField(unique=True, max_length=255, allow_unicode=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = create_input_title_slug(self)
        return super().save(*args, **kwargs)


class Entity(models.Model):
    title = models.JSONField(default=default_title)
    slug = models.SlugField(unique=True, max_length=255, allow_unicode=True)
    config = models.JSONField(default=default_config)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = create_title_slug(self)
        return super().save(*args, **kwargs)

class Marka(models.Model):
    label = models.JSONField(default=default_label)
    slug = models.SlugField(unique=True, max_length=255, allow_unicode=True)
    image = models.ImageField(upload_to='marka_i', null=True, blank=True)
    category = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    sorting = models.IntegerField(null=False, blank=False, default=100)

    def __str__(self):
        return self.label.get("label_uz", "")

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['mptt_level']

    def save(self, *args, **kwargs):
        self.slug = create_label_slug(self)
        return super().save(*args, **kwargs)

class Model(models.Model):
    label = models.JSONField(default=default_label)
    slug = models.SlugField(unique=True, max_length=255, allow_unicode=True)
    parent = models.ForeignKey(Marka, on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    sorting = models.IntegerField(null=False, blank=False, default=100)

    def __str__(self):
        return self.label.get("label_uz", "")

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['mptt_level']

    def save(self, *args, **kwargs):
        self.slug = create_label_slug(self)
        return super().save(*args, **kwargs)

class Positsion(models.Model):
    label = models.JSONField(default=default_label)
    slug = models.SlugField(max_length=255, allow_unicode=True)
    parent = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.label.get("label_uz", "")

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['mptt_level']

    def save(self, *args, **kwargs):
        self.slug = create_label_slug(self)
        return super().save(*args, **kwargs)

class Attribute(models.Model):
    input_type = models.ForeignKey(
        InputType, related_name="attribute_input_type", blank=False, null=True, on_delete=models.SET_NULL
    )
    slug = models.SlugField(unique=True, max_length=255, allow_unicode=True)
    properties = models.JSONField(default=default_properties)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    is_price = models.BooleanField(default=False, null=False, blank=False)
    price_state = models.PositiveIntegerField(
        default=1, null=False, blank=False,
        choices=[(1, "NONE PRICE FIELD"), (3, "FROM-TO"), (4, "PRICE"), (5, "CURRENCY")]
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.slug

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['mptt_level']

    def save(self, *args, **kwargs):
        self.slug = create_attribute_slug(self)
        return super().save(*args, **kwargs)


class Value(models.Model):
    label = models.JSONField(default=default_label)
    slug = models.SlugField(unique=True, max_length=255, allow_unicode=True)
    image = models.ImageField(upload_to='value', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.label.get("label_uz", "")

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['mptt_level']

    def save(self, *args, **kwargs):
        self.slug = create_label_slug(self)
        return super().save(*args, **kwargs)


class CategoryEntity(models.Model):
    category = models.ForeignKey(
        Category, related_name="category_ce", blank=False, null=True, on_delete=models.SET_NULL
    )
    entity = models.ForeignKey(
        Entity, related_name="entity_ce", blank=False, null=True, on_delete=models.SET_NULL
    )
    sorting = models.PositiveIntegerField(blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        unique_together = ("category", "entity")

    def __str__(self):
        return f"{self.sorting}. {self.category.slug} - {self.entity.slug}"


class EntityAttribute(models.Model):
    entity = models.ForeignKey(
        Entity, related_name="entity_ea", blank=False, null=True, on_delete=models.SET_NULL
    )
    attribute = models.ForeignKey(
        Attribute, related_name="attribute_ea", blank=False, null=True, on_delete=models.SET_NULL
    )
    sorting = models.PositiveIntegerField(blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        unique_together = ("entity", "attribute",)

    def __str__(self):
        return f"{self.sorting}. {self.entity.slug} - {self.attribute.slug}"


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute, related_name="attribute_av", blank=False, null=True, on_delete=models.SET_NULL
    )
    value = models.ForeignKey(
        Value, related_name="value_av", blank=False, null=True, on_delete=models.SET_NULL
    )
    sorting = models.PositiveIntegerField(blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        unique_together = ("attribute", "value")

    def __str__(self):
        return f"{self.sorting}. {self.attribute.slug} - {self.value.slug}"

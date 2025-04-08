from datetime import datetime
from text_unidecode import unidecode
from django.utils.text import slugify


def create_title_slug(instance):
    slug = instance.slug
    if slug is None or slug == "":
        slug = slugify(unidecode(instance.title.get("title_uz")))
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        if Klass.objects.get(slug=slug).pk != instance.pk:
            slug = slugify("{}-{}".format(unidecode(instance.title.get("title_uz")), datetime.now().timestamp()))
    return slug


def create_input_title_slug(instance):
    slug = instance.slug
    if slug is None or slug == "" and not instance.pk:
        slug = slugify(unidecode(instance.title))
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        if Klass.objects.get(slug=slug).pk != instance.pk:
            slug = slugify("{}-{}".format(unidecode(instance.title), datetime.now().timestamp()))
    return slug


def create_label_slug(instance):
    slug = instance.slug
    if slug is None or slug == "" and not instance.pk:
        slug = slugify(unidecode(instance.label.get("label_uz")))
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        if Klass.objects.get(slug=slug).pk != instance.pk:
            slug = slugify("{}-{}".format(unidecode(instance.label.get("label_uz")), datetime.now().timestamp()))
    return slug


def create_attribute_slug(instance):
    slug = instance.slug
    if slug is None or slug == "" and not instance.pk:
        slug = slugify(unidecode(instance.properties.get("label", {}).get("label_uz")))
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        if Klass.objects.get(slug=slug).pk != instance.pk:
            slug = slugify("{}-{}".format(unidecode(instance.properties.get("label", {}).get("label_uz")), datetime.now().timestamp()))
    return slug

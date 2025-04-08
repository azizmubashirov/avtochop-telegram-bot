from datetime import datetime
from text_unidecode import unidecode
from django.utils.text import slugify


def create_title_slug(instance):
    slug = instance.slug
    if slug is None or slug == "":
        slug = slugify(unidecode(instance.title))
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        if Klass.objects.get(slug=slug).pk != instance.pk:
            slug = slugify("{}-{}".format(unidecode(instance.title), datetime.now().timestamp()))
    return slug


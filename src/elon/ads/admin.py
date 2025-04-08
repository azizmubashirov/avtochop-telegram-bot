from django.contrib import admin
from .models import Ad, AdFilter

class AdAdmin(admin.ModelAdmin):
    def price(self, object):
        try:
            data = object.prices['narx']
        except Exception as e:
            data = object.prices
        return data
    list_display = ("id", "title", "category", "region", "district", "created_at", "user", "price")
    fields = ("title", "slug", "category", "description", "images",
              "prices", "properties", "contact", "region", "district",
              "status", "moderated", "views_count", "currency",
              "updated_at", "deleted_at",
              )
    search_fields = ['id', 'prices__narx']

class AdFiltersAdmin(admin.ModelAdmin):
    list_display = ("category", "properties")



admin.site.register(Ad, AdAdmin)
admin.site.register(AdFilter, AdFiltersAdmin)

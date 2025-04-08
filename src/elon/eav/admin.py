from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import (Category, InputType, Entity, Attribute, Value, CategoryEntity, EntityAttribute, AttributeValue, Marka, Model, Positsion)

class CategoryAdmin(MPTTModelAdmin):
    list_display = ("title", "slug", "sorting")

class InputTypeAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")

class EntityAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "config")

class AttributeAdmin(admin.ModelAdmin):
    list_display = ("input_type", "slug", "parent")


class ValueAdmin(admin.ModelAdmin):
    list_display = ("label", "slug", "parent")
    readonly_fields = ('id',)

class CategoryEntityAdmin(admin.ModelAdmin):
    list_display = ("category", "entity", "sorting")

class EntityAttributeAdmin(admin.ModelAdmin):
    list_display = ("entity", "attribute", "sorting")
    
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("value", "attribute", "sorting")

class MarkaAdmin(admin.ModelAdmin):
    list_display = ("label", "slug", "sorting", "category")

class ModelAdmin(admin.ModelAdmin):
    list_display = ("label", "slug", "sorting", "parent")

class PositsionAdmin(admin.ModelAdmin):
    list_display = ("label", "slug", "parent")

admin.site.register(Category, CategoryAdmin)
admin.site.register(InputType, InputTypeAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Value, ValueAdmin)
admin.site.register(CategoryEntity, CategoryEntityAdmin)
admin.site.register(EntityAttribute, EntityAttributeAdmin)
admin.site.register(AttributeValue, AttributeValueAdmin)
admin.site.register(Marka, MarkaAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Positsion, PositsionAdmin)

